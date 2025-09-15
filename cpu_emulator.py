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
            return -1
        else:
            self.hp+=rdi
            self.cpu.registers[rax]=self.hp
            return 0


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


    
    
        