#!/usr/bin/env python3


class Memory:
    def __init__(self,size,cpu: Cpu):
        self.memory=bytearray(size)
        self.size=size
        self.sp=size
        self.hp=0
        self.heapBlocks={}
        self.cpu=cpu

    def stack_push(self,data: bytes):
        lent=len(data)
        self.sp-=lent
        self.memory[self.sp:self.sp+n]=data
        self.cpu.registers[rsp]=self.sp

    def stack_pop(self,n: int):
        data=memory[self.sp:self.sp+n]
        self.sp+=n
        self.cpu.registers[rsp]=self.sp
        return data

    def write_to_heap(self,rax,rdi):
        if rdi<0:
            return None
        else:
            self.hp+=rdi
            self.cpu.registers[rax]=self.hp

class Cpu:
    def __init__(self,instructionPointer,memory: Memory):
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
        if registerid in self.registers:
            self.registers[registerid]=value
        elif '[' in registerid and ']' in registerid:
            registerid=registerid.replace('[','').replace(']','')
            self.memory.memory[registerid]=value
    
    def get_register_value(self,registerid):
        if registerid in self.registers:
            try:
                return value=self.registers[registerid]
            except:
                return None
        elif '[' in registerid and ']' in registerid:
            registerid=registerid.replace('[','').replace(']','')
            return value=self.memory.memory[registerid]
        else:
            return registerid

    def ALU_Unit(self,operation,arg1,arg2):
        if arg1 in self.registers or arg2 in self.registers or ('[' in arg2 and ']'in arg2):
            match operation:
                case '+':
                    set_register_value(arg2,get_register_value(arg1)+get_register_value(arg2))
                case '-':
                    set_register_value(arg2,get_register_value(arg1)-get_register_value(arg2))
                case '*':
                    set_register_value(arg2,get_register_value(arg1)*get_register_value(arg2))
                case '/':
                    set_register_value(arg2,get_register_value(arg1)/get_register_value(arg2))
                case 'or':
                    set_register_value(arg2,get_register_value(arg1)|get_register_value(arg2))
                case 'and':
                    set_register_value(arg2,get_register_value(arg1)&get_register_value(arg2))
                case 'xor':
                    set_register_value(arg2,get_register_value(arg1)^get_register_value(arg2))
        

