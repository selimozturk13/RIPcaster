section .data
msg db "Hello Emulator", 10, 0

section .text
global _start
_start:
mov rax, 10
mov rbx, 5
add rax, rbx
sub rax, 3
xor rcx, rcx
or rcx, rax
and rcx, 15
inc rcx
dec rcx
lea rdx, [rax + 4]
push rax
push rdx
pop rsi
pop rdi
mov rax, 1
mov rdi, 1
lea rsi, [msg]
mov rdx, 15
syscall
mov rax, 60
xor rdi, rdi
syscall