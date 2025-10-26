section .data
msg db "hello world jmp function is working", 10, 0

section .text
_start:
    mov rax, 1          ; RAX = 1
    jmp skip            ; jump to label 'skip'
    mov rax, 2          ; this line must be skipped
    mov rax, 3          ; this too
skip:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg
    mov rdx, 37
    syscall
    mov rax, 5          ; execution should land here
    mov rdi, 0
    mov rax, 60         ; exit syscall (rax = 60)
    syscall