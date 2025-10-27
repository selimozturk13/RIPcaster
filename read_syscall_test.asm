section .data
readmsg db ">>> ",0
section .bss
    buffer resq 8      ; 64 byte'lık buffer (okunan veri buraya yazılacak)

section .text
    global _start

_start:
    mov rax, 1
    mov rdi, 1
    mov rsi, readmsg
    mov rdx, 5
    syscall
    ; read(0, buffer, 64)
    mov rax, 0            ; syscall number for read
    mov rdi, 0            ; file descriptor: stdin
    mov rsi, buffer       ; buffer address
    mov rdx, 64           ; max bytes to read
    syscall

    ; rax = okunan byte sayısı
    mov rdi, 1            ; stdout
    mov rsi, buffer       ; yazılacak veri
    mov rdx, rax          ; read'in döndürdüğü kadar yaz
    mov rax, 1            ; syscall number for write
    syscall

    ; exit(0)
    mov rax, 60           ; syscall number for exit
    xor rdi, rdi          ; status = 0
    syscall