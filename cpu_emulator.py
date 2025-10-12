#!/usr/bin/env python3
import sys
import tomllib

class Memory:
    def __init__(self,size,cpu):
        self.memory=bytearray(size)
        self.size=size
        self.sp=size
        self.hp=0
        self.heapBlocks={}
        self.cpu=cpu

    def stack_push(self,data: bytes):
        self.sp-=8
        self.memory[self.sp:self.sp-8]=data
        self.cpu.registers["rsp"]=self.sp

    def stack_pop(self):
        data=memory[self.sp:self.sp+8]
        self.sp+=8
        self.cpu.registers["rsp"]=self.sp
        return data

    def write_to_heap(self,rax,rdi):
        if rdi<0:
            return None
        else:
            self.hp+=rdi
            self.cpu.registers[rax]=self.hp
    def get_memory(self,addr):
        try:
            return self.memory[addr]
        except:
            print(f"RIP: {self.cpu.instructionPointer}",file=sys.stderr)

class Cpu:
    def __init__(self,instructionPointer,memory):
        self.instructionPointer=instructionPointer
        self.memory=memory
        self.registers={
            "rax":0,
            "rbx":0,
            "rcx":0,
            "rdx":0,
            "rsi":0,
            "rdi":0,
            "rbp":0,
            "rsp":0
        }
        self.zeroFlag=0

#elif '[' in registerid and ']' in registerid:
#           registerid=registerid.replace('[','').replace(']','')

    def set_register_value(self,registerid,value):
        if str(registerid) in self.registers:
            self.registers[registerid]=value
        elif '[' in str(registerid) and ']' in str(registerid):
            registerid=registerid.replace('[','').replace(']','')
            self.memory.memory[registerid]=value
        elif '\'' in registerid and '\'' in registerid:
            self.memory.memory[registerid]=ord(value)
    
    def get_register_value(self,registerid):
        if str(registerid) in self.registers:
            try:
                return self.registers[registerid]
            except:
                return None
        elif '[' in str(registerid) and ']' in str(registerid):
            registerid=registerid.replace('[','').replace(']','')
            return self.memory.memory[registerid]
        else:
            return registerid

    def ALU_Unit(self,operation,arg1,arg2):
        if str(arg1) in self.registers or str(arg2) in self.registers or ('[' in str(arg2) and ']'in str(arg2)):
            
            match operation:
                case '+':
                    self.set_register_value(arg1,int(self.get_register_value(arg1))+int(self.get_register_value(arg2)))
                case '-':
                    self.set_register_value(arg1,int(self.get_register_value(arg1))-int(self.get_register_value(arg2)))
                case '*':
                    self.set_register_value(arg2,int(self.get_register_value(arg1))*int(self.get_register_value(arg2)))
                case '/':
                    self.set_register_value(arg2,int(self.get_register_value(arg1))/int(self.get_register_value(arg2)))
                case 'or':
                    self.set_register_value(arg1,int(self.get_register_value(arg1))|int(self.get_register_value(arg2)))
                case 'and':
                    self.set_register_value(arg1,int(self.get_register_value(arg1))&int(self.get_register_value(arg2)))
                case 'xor':
                    self.set_register_value(arg2,int(self.get_register_value(arg1),base=2)^int(self.get_register_value(arg2),base=2))
        

class mem:
    def __init__(self,a):
        self.a=a

try:
    with open("config.toml","rb") as f:
        config_data=tomllib.load(f)
except OSError as err:
    print(f"open: {err.strerror}",file=sys.stderr)
    sys.exit(-1)
ram_size=config_data["hardware"]["ram_size"]
asmfile=config_data["files"]["asmfile"]

try:
    with open(asmfile,"r") as f:
        asmdata=f.read()
except OSError as err:
    print(f"open: {err.strerror}",file=sys.stderr)
    sys.exit(-1)
asmlines=asmdata.split("\n")
instructions=[]
i=0
for line in asmlines:
    line=line.replace(",","")
    instructions.append(line)
    if line=="_start:":
        inspoint=i
    i+=1

a=mem(1)
cpu=Cpu(inspoint,a)
memory=Memory(ram_size,cpu)
cpu.memory=memory



while instructions[cpu.instructionPointer]!="halt":
    instruction_line=instructions[cpu.instructionPointer]
    instruction_parts=instruction_line.split()
    instruction=instruction_parts[0]
    arg1=instruction_parts[1] if len(instruction_parts)>1 else None
    arg2=instruction_parts[2] if len(instruction_parts)>2 else None
    
    match instruction:
        case "ADD":
            cpu.ALU_Unit("+",arg1,arg2)   
        case "SUB":
            cpu.ALU_Unit("-",arg1,arg2)
        case "MUL":
            cpu.ALU_Unit("*",arg1,"rax")
        case "DIV":
            cpu.ALU_Unit("/",arg1,"rax")
        case "AND":
            cpu.ALU_Unit("and",arg1,arg2)
        case "OR":
            cpu.ALU_Unit("or",arg1,arg2)
        case "XOR":
            cpu.ALU_Unit("xor",arg1,arg2)
        case "MOV":
            cpu.set_register_value(arg1,cpu.get_register_value(arg2))
        case "INC":
            cpu.set_register_value(arg1,(int(cpu.get_register_value(arg1))+1))
        case "DEC":
            cpu.set_register_value(arg1,(int(cpu.get_register_value(arg1))-1))
        case "syscall":  
            match ord(cpu.get_register_value("rax")):
                case 0x2000004:
                    rdi=ord(cpu.get_register_value("rdi"))
                    if rdi==1:
                        i=0
                        while(i<cpu.get_register_value("rdx")):
                            try:
                                print(chr(memory.get_memory(cpu.get_register_value("rax")+i)))
                                rdx+=1
                            except:
                                print(f"RIP: {cpu.instructionPointer}",file=sys.stderr)
                    elif rdi==2:
                        try:
                            i=0
                            while(i<cpu.get_register_value("rdx")):
                                print(chr(memory.get_memory(cpu.get_register_value("rax")+i)),file=sys.stderr)
                                rdx+=1
                        except:
                            print(f"RIP: {cpu.instructionPointer}",file=sys.stderr)
                case 0x2000001:
                    sys.exit(cpu.get_register_value("rdi"))

    cpu.instructionPointer+=1   