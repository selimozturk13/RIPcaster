section .data
    msg1 db "Enter a number: ", 0
    msg2 db "You entered: ", 0
    newline db 10, 0
    stack_msg db "Stack top: ", 0

section .bss
    inputbuf resq 4        ; 32 byte buffer
    tempval resq 1         ; 8 byte temp

section .text
    global _start

_start:
    ; ---------- WRITE "Enter a number: " ----------
    mov rax, 1
    mov rdi, 1
    mov rsi, msg1
    mov rdx, 16
    syscall

    ; ---------- READ 32 BYTE ----------
    mov rax, 0
    mov rdi, 0
    mov rsi, inputbuf
    mov rdx, 32
    syscall                 ; rax = okunan byte sayısı
    push rax
    ; ---------- WRITE "You entered: " ----------
    mov rax, 1
    mov rdi, 1
    mov rsi, msg2
    mov rdx, 13
    syscall

    ; ---------- WRITE inputbuf ----------
    mov rax, 1
    mov rdi, 1
    mov rsi, inputbuf
    pop rdx
    syscall

    ; ---------- NEWLINE ----------
    mov rax, 1
    mov rdi, 1
    mov rsi, newline
    mov rdx, 1
    syscall

    ; ---------- STACK TEST ----------
    mov rax, 42
    push rax                 ; push 42
    mov rax, 84
    push rax                 ; push 84

    pop rbx                  ; rbx = 84
    
    pop rcx                  ; rcx = 42
    

    ; ---------- WRITE stack_msg ----------
    mov rax, 1
    mov rdi, 1
    mov rsi, stack_msg
    mov rdx, 11
    syscall

    ; ---------- WRITE stack top (rbx) ----------
    mov rax, 1
    mov rdi, 1
    lea rsi, [stacktest]     ; rsi = stacktest address
    mov rdx, 16
    syscall

    ; ---------- ARİTMETİK TESTLERİ ----------
    mov rax, 10
    mov rbx, 3
    add rax, rbx             ; rax = 13
    sub rax, 2               ; rax = 11
    mul rbx                  ; rax = 33
    div rbx                  ; rax = 11

    ; ---------- CMP & JE TESTİ ----------
    mov rcx, 11
    cmp rax, rcx
    je equal_label

    ; eşit değilse
    mov rax, 1
    mov rdi, 1
    mov rsi, msg1
    mov rdx, 16
    syscall
    jmp end_program

equal_label:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg2
    mov rdx, 13
    syscall

end_program:
    ; ---------- EXIT ----------
    mov rax, 60
    xor rdi, rdi
    syscall
