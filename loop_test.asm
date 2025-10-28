section .data
   msg1 db "Starting loop!", 10
   msg2 db "Finally ended!", 10
   msg3 db "loop is running",10,0
section .text
_start:
   mov rax, 1
   mov rsi, msg1
   mov rdi, 1
   mov rdx, 15
   syscall
   xor rcx, rcx
   mov rdi, 2
asm_loop:
   mov rsi, msg3
   mov rdx, 17
   syscall
   inc rcx
   cmp rcx, 100000
   jne asm_loop
   mov rax, 1
   mov rdi, 1
   mov rdx, 15
   mov rsi, msg2
   syscall
   xor rdi, rdi
   mov rax, 60
   syscall