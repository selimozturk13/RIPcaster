section .data
global _start
_start:
MOV rax, 10
MOV rbx, 10
MUL rbx
MOV rsi, rax
MOV rax, 1
MOV rdi, 1
MOV rdx, 3
syscall
MOV rax, 10
MOV rbx, 10
ADD rax, rbx
MOV rsi, rax
MOV rax, 1
MOV rdi, 1
MOV rdx, 2
syscall
MOV rax, 10
MOV rbx, 10
SUB rax, rbx
MOV rsi, rax
MOV rax, 1
MOV rdi, 1
MOV rdx, 1
syscall
MOV rax, 10
MOV rbx, 10
DIV rbx
MOV rsi, rax
MOV rax, 1
MOV rdi, 1
MOV rdx, 3
syscall
MOV rax, 10
MOV rbx, 10
AND rax, rbx
MOV rsi, rax
MOV rax, 1
MOV rdi, 1
MOV rdx, 2
syscall
MOV rax, 10
MOV rbx, 10
OR rax, rbx
MOV rsi, rax
MOV rax, 1
MOV rdi, 1
MOV rdx, 2
syscall
MOV rax, 10
XOR rax, rax
MOV rsi, rax
MOV rax, 1
MOV rdi, 1
MOV rdx, 1
syscall
MOV rax, 10
INC rax
MOV rsi, rax
MOV rax, 1
MOV rdi, 1
MOV rdx, 2
syscall
MOV rax, 10
DEC rax
MOV rsi, rax
MOV rax, 1
MOV rdi, 1
MOV rdx, 1
syscall
halt