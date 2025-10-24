section .data
msg db "Hello Emulator", 10

section .text
global _start
_start:
mov rax, 1
mov rdi, 1
lea rsi, [msg]
mov rdx, 15
syscall
mov rax, 60
xor rdi, rdi
syscall