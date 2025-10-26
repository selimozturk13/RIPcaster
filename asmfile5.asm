section .data
errmsg db "this is an error message", 10, 0

section .text
_start:
mov rax, 1
mov rdx, 3
div rdx
jmp error
error:
mov rax, 1
mov rdi, 2
lea rsi, errmsg
mov rdx, 25
syscall
mov rax, 60
mov rdi, -1
syscall
