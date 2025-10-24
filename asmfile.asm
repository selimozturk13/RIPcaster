section .data
    msg_hello db "Hello stack!", 10, 0
    msg_stack  db "Stack test done", 10, 0
    newline    db 10, 0

section .text
_start:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg_hello
    mov rdx, 13
    syscall

    mov rax, 10
    mov rbx, 20

    push rax
    push rbx

    pop rcx
    pop rdx

    add rcx, rdx

    mov rax, 1
    mov rdi, 1
    mov rsi, newline
    mov rdx, 1
    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, msg_stack
    mov rdx, 16
    syscall

    mov rax, 60
    mov rdi, 0
    syscall
