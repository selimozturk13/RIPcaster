#!/usr/bin/env python3
import sys
import tomllib
import os


class Memory:
    def __init__(self,size,cpu):
        self.datasection={}
        self.memory=bytearray(size)
        self.size=size
        self.sp=size
        self.hp=0
        self.heapBlocks={}
        self.cpu=cpu

    def stack_push(self, data):
        if isinstance(data, int):
            data = data.to_bytes(8, byteorder='little', signed=True)
        elif isinstance(data, str):
            data = data.encode('utf-8')
        elif not isinstance(data, (bytes, bytearray)):
            raise TypeError(f"Unsupported type pushed to stack: {type(data)}")

        self.sp -= len(data)
        self.memory[self.sp:self.sp + len(data)] = data
        self.cpu.registers["rsp"] = self.sp

    def stack_pop(self):
        data = self.memory[self.sp:self.sp + 8]
        self.sp += 8
        self.cpu.registers["rsp"] = self.sp
        return int.from_bytes(data, byteorder='little', signed=True)

    def write_to_heap(self,rax,rdi):
        rdi=self.cpu.get_register_value(rdi)
        if rdi<0:
            return None
        else:
            self.hp+=rdi
            self.cpu.registers[rax]=self.hp

    def get_memory(self,addr):
        if isinstance(addr, str):
            try:
                addr = int(addr, 0)
            except:
                data = self.datasection.get(addr)
                if data:
                    addr = data[0]
                else:
                    raise ValueError(f"Unknown label {addr}")
        return self.memory[addr]
    def add_data_to_data_section(self,name,data,size):
        try:
            if not self.datasection:
                pointer = 0
            else:
                pointer = list(self.datasection.values())[-1][0] + list(self.datasection.values())[-1][1]
            lent = size
            if isinstance(data, str):
                data = data.encode('utf-8')
            self.memory[pointer:pointer+lent] = data
            self.hp+=lent
            self.datasection[name] = [pointer, lent]
        except Exception as e:
            print("Data adding error:", e)
    def get_data_from_data_section(self,name):
        return self.datasection.get(name)

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
        self.signFlag = 0
        self.carryFlag = 0
        self.overflowFlag = 0
        self.parityFlag=0

    def set_register_value(self,registerid,value):
        if str(registerid) in self.registers:
            self.registers[registerid]=value
        elif '[' in str(registerid) and ']' in str(registerid):
            
            registerid=registerid.replace('[','').replace(']','')
            self.memory.memory[registerid]=value.encode() if isinstance(value,str) else value
        elif '\'' in registerid and '\'' in registerid:
            self.memory.memory[registerid]=ord(value)
    
    def get_register_value(self,registerid):
        if isinstance(registerid, str) and registerid.isdigit():
            val = int(registerid)
            return val
        elif str(registerid) in self.registers:
            try:
                return self.registers[registerid]
            except Exception as err:
                print(f"RIP : {self.registers["rip"]}\n{err}")
                sys.exit(-1)
        elif '[' in str(registerid) and ']' in str(registerid) and '+' in str(registerid):
            #relative addressing
            registerid=registerid.replace('[','').replace(']','')
            registerid=registerid.split('+')
            try:
                registerval=self.registers[registerid[0]]
            except:
                try:
                    return self.memory.memory[int(registerid[0])+int(registerid[1])]
                except Exception as err:
                    print(f"RIP : {self.registers["rip"]}\n{err}")
                    os._exit(-1)
            else:
                try:
                    data=self.memory.get_data_from_data_section(registerid[1])
                except:
                    try:
                        global instructions
                        i=0
                        for instruction in instructions:
                            if instruction==registerid[1].replace(':',''):
                                break
                            i+=1
                        offset=i-registerval
                        return registerval+offset
                    except Exception as err:
                        print(f"RIP : {self.registers["rip"]}\n{err}")
                        os._exit(-1)
                else:
                    offset=data[0]-self.registers["rip"]
                    return self.registers["rip"]+data[0]

        elif '[' in str(registerid) and ']' in str(registerid):
            registerid=registerid.replace('[','').replace(']','')
            return self.memory.memory[registerid]
        elif registerid in self.memory.datasection:
            return self.memory.get_data_from_data_section(registerid)[0]
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
                    self.set_register_value(arg2,int(self.get_register_value(arg1))^int(self.get_register_value(arg2)))
    def jump(self,label):
        if type(label)==int:
            print(f"RIP: {self.get_register_value("rip")}")
            raise ValueError("A label can not be an integer.")
        global instructions
        i=0
        for instruction118 in instructions:
            if label==instruction118:
                self.set_register_value("rip",i)
                break
            i+=1
        

class mem:
    def __init__(self,a):
        self.a=a

try:
    with open("config.toml","rb") as f:
        config_data=tomllib.load(f)
except OSError as err:
    print(f"open: {err.strerror}",file=sys.stderr)
    os._exit(-1)
ram_size=config_data["hardware"]["ram_size"]
asmfile=config_data["files"]["asmfile"]

try:
    with open(asmfile,"r") as f:
        asmdata=f.read()
except OSError as err:
    print(f"open: {err.strerror}",file=sys.stderr)
    os._exit(-1)

instructions=asmdata.split("\n")
i=0
for line in instructions:
    line=line.replace(",","")
    
    if line=="_start:":
        inspoint=i
    if line=="section .data":
        dataptr=i
    if line=="section .bss":
        bssptr=i
    i+=1


a=mem(1)
cpu=Cpu(inspoint,a)
memory=Memory(ram_size,cpu)
cpu.memory=memory

while True:
    try:
        dataline = instructions[dataptr].strip()
    except:
        break
    else:
        try:
            if dataline == "section .text" or dataline=="section .bss":
                break

            if not dataline or dataline.startswith(";"):
                dataptr += 1
                continue

            parts = dataline.split(None, 2)  
            if len(parts) < 3:
                dataptr += 1
                continue

            name, typeofvar, raw_data = parts
            if typeofvar != "db":
                dataptr += 1
                continue

            data = bytearray()

            
            tokens = [x.strip() for x in raw_data.split(",")]

            for token in tokens:
                if token.startswith('\"') and token.endswith('\"'):
                
                    text = token.strip('"')
                    data.extend(text.encode('utf-8'))
                elif token.isdigit():
                    data.append(int(token))
                else:
                    raise ValueError(f"Unsupported db value: {token}")

            memory.add_data_to_data_section(name, data, len(data))
            dataptr += 1
        except Exception as e:
            print("DATA ERROR:", e)
            break

while True:
 
    try:
        bssline=instructions[bssptr].strip()
    except:
        break
    else:
        #name size times
        if bssline=="section .data" or bssline=="section .text":
            break
        if not bssline or bssline.startswith(";"):
            bssptr+=1
            continue
        bssline=bssline.split()
        if len(bssline)<3:
            bssptr+=1
            continue
        name=bssline[0]
        size=bssline[1]
        times=bssline[2]
        if size!="resq":
            bssptr+=1
            continue
        memory.add_data_to_data_section(name,(8*int(times))*b"\x00",8*int(times))
        bssptr+=1

while cpu.instructionPointer<len(instructions):
    instruction_line=instructions[cpu.instructionPointer].replace(",","")
    instruction_parts=instruction_line.split()
    instruction=instruction_parts[0].lower() if len(instruction_parts)>=1 else None
    arg1=instruction_parts[1].lower() if len(instruction_parts)>1 else None
    arg2=instruction_parts[2].lower() if len(instruction_parts)>2 else None
   
    match instruction:
     
        case "add":
            cpu.ALU_Unit("+",arg1,arg2)   
        case "sub":
            cpu.ALU_Unit("-",arg1,arg2)
        case "mul":
            cpu.ALU_Unit("*",arg1,"rax")
        case "div":
            cpu.ALU_Unit("/",arg1,"rax")
        case "and":
            cpu.ALU_Unit("and",arg1,arg2)
        case "or":
            cpu.ALU_Unit("or",arg1,arg2)
        case "xor":
            cpu.ALU_Unit("xor",arg1,arg2)
        case "mov":
            val = cpu.get_register_value(arg2)
            if isinstance(val, str) and val.isdigit():
                val = int(val)
            cpu.set_register_value(arg1, val)
        case "inc":
            cpu.set_register_value(arg1,(int(cpu.get_register_value(arg1))+1))
        case "dec":
            cpu.set_register_value(arg1,(int(cpu.get_register_value(arg1))-1))
        case "push":
            memory.stack_push(cpu.get_register_value(arg1))
        case "pop":
            cpu.set_register_value(arg1,memory.stack_pop())
        case "lea":
            arg2 = arg2.replace("[","").replace("]","")
            if arg2 in memory.datasection:
                cpu.set_register_value(arg1, memory.get_data_from_data_section(arg2)[0])
            else:
                i = 0
                for instruction314 in instructions:
                    if instruction314 == arg2:
                        break
                    i += 1
                cpu.set_register_value(arg1, i)  
        case "jmp":
            try:
                cpu.jump(cpu.get_register_value(arg1))  
            except:
                raise  
        case "cmp":
            arg1=int(cpu.get_register_value(arg1))
            arg2=int(cpu.get_register_value(arg2))
            result=arg1-arg2
            cpu.zeroFlag=int(result==0)
            cpu.signFlag=int(result<0)
            cpu.carryFlag=int((arg1 & 0xFFFFFFFFFFFFFFFF) < (arg2 & 0xFFFFFFFFFFFFFFFF))
            cpu.overflowFlag=int(result>127 or result<-127)
        case "je" | "jz": 
            if cpu.zeroFlag==1:
                try:
                    cpu.jump(cpu.get_register_value(arg1))  
                except:
                    raise 
        case "jne" | "jnz":
            if cpu.zeroFlag!=1:
                try:
                    cpu.jump(cpu.get_register_value(arg1))  
                except:
                    raise 
        case "jg" | "jnle":
            if cpu.signFlag==cpu.overflowFlag or cpu.zeroFlag==0:
                try:
                    cpu.jump(cpu.get_register_value(arg1))  
                except:
                    raise 
        case "jge" | "jnl":
            if cpu.signFlag==cpu.overflowFlag:
                try:
                    cpu.jump(cpu.get_register_value(arg1))  
                except:
                    raise 
        case "jl" | "jnge":
            if cpu.signFlag!=cpu.overflowFlag:
                try:
                    cpu.jump(cpu.get_register_value(arg1))  
                except:
                    raise 
        case "jle" | "jng":
            if cpu.signFlag!=cpu.overflowFlag or cpu.zeroFlag==1:
                try:
                    cpu.jump(cpu.get_register_value(arg1))  
                except:
                    raise 
        case "ja" | "jnbe":
            if cpu.carryFlag == 0 and cpu.zeroFlag == 0:
                try:
                    cpu.jump(cpu.get_register_value(arg1))
                except:
                    raise
        case "jae" | "jnb":
            if cpu.carryFlag == 0:
                try:
                    cpu.jump(cpu.get_register_value(arg1))
                except:
                    raise
        case "jb" | "jnae":
            if cpu.carryFlag == 1:
                try:
                    cpu.jump(cpu.get_register_value(arg1))
                except:
                    raise
        case "jbe" | "jna":
            if cpu.carryFlag == 1 or cpu.zeroFlag == 1:
                try:
                    cpu.jump(cpu.get_register_value(arg1))
                except:
                    raise
        case "jo":
            if cpu.overflowFlag == 1:
                try:
                    cpu.jump(cpu.get_register_value(arg1))
                except:
                    raise
        case "jno":
            if cpu.overflowFlag == 0:
                try:
                    cpu.jump(cpu.get_register_value(arg1))
                except:
                    raise
        case "js":
            if cpu.signFlag == 1:
                try:
                    cpu.jump(cpu.get_register_value(arg1))
                except:
                    raise
        case "jns":
            if cpu.signFlag == 0:
                try:
                    cpu.jump(cpu.get_register_value(arg1))
                except:
                    raise
        case "jp" | "jpe":
            if cpu.parityFlag == 1:
                try:
                    cpu.jump(cpu.get_register_value(arg1))
                except:
                    raise
        case "jnp" | "jpo":
            if cpu.parityFlag == 0:
                try:
                    cpu.jump(cpu.get_register_value(arg1))
                except:
                    raise
        case "syscall":  
            
            rax= cpu.get_register_value("rax") if isinstance(cpu.get_register_value("rax"),int) else ord(cpu.get_register_value("rax"))
            #write syscall
            if rax == 1:
                fd = cpu.get_register_value("rdi")
                buf = cpu.get_register_value("rsi")
                length = cpu.get_register_value("rdx")
                if fd == 1:
                    for i in range(length):
                        sys.stdout.write(chr(memory.get_memory(buf + i)))
                    sys.stdout.flush()
                if fd == 2:
                    for i in range(length):
                        sys.stderr.write(chr(memory.get_memory(buf + i)))
                    sys.stderr.flush()
            
            #get input syscall
            if rax==0:
                fd=cpu.get_register_value("rdi")
                if fd==0:
                    buf=cpu.get_register_value("rsi")
                    maxsize=cpu.get_register_value("rdx")
                    user_input=sys.stdin.readline(maxsize)
                    memory.memory[int(buf):int(buf)+len(user_input)] = user_input.encode()
                    cpu.set_register_value("rax",len(user_input))
            #exit syscall 
            if rax==60:
                sys.exit(cpu.get_register_value("rdi"))
        case "halt":
            break
    cpu.instructionPointer+=1   

