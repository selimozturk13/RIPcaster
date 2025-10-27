section .data
msg_equal db "JE/JZ worked", 10, 0
msg_notequal db "JNE/JNZ worked", 10, 0
msg_greater db "JG/JNLE worked", 10, 0
msg_ge db "JGE/JNL worked", 10, 0
msg_less db "JL/JNGE worked", 10, 0
msg_le db "JLE/JNG worked", 10, 0
msg_ja db "JA/JNBE worked", 10, 0
msg_jae db "JAE/JNB worked", 10, 0
msg_jb db "JB/JNAE worked", 10, 0
msg_jbe db "JBE/JNA worked", 10, 0
msg_jo db "JO worked", 10, 0
msg_jno db "JNO worked", 10, 0
msg_js db "JS worked", 10, 0
msg_jns db "JNS worked", 10, 0
msg_jp db "JP/JPE worked", 10, 0
msg_jnp db "JNP/JPO worked", 10, 0
msg db "Hello Emulator", 10, 0
msg_hello db "Hello stack!", 10, 0
msg_stack  db "Stack test done", 10, 0
newline    db 10, 0


section .text
_start:
; -------- ZF test --------
mov rax, 5
mov rbx, 5
cmp rax, rbx
je je_label
jne jne_label

je_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_equal
mov rdx, 14
syscall

jne_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_notequal
mov rdx, 17
syscall

; -------- Signed comparison test --------
mov rax, 10
mov rbx, 5
cmp rax, rbx
jg jg_label
jge jge_label
jl jl_label
jle jle_label

jg_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_greater
mov rdx, 16
syscall

jge_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_ge
mov rdx, 15
syscall

jl_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_less
mov rdx, 15
syscall

jle_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_le
mov rdx, 15
syscall

; -------- Unsigned comparison test --------
mov rax, 5
mov rbx, 10
cmp rax, rbx
ja ja_label
jae jae_label
jb jb_label
jbe jbe_label

ja_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_ja
mov rdx, 15
syscall

jae_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_jae
mov rdx, 16
syscall

jb_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_jb
mov rdx, 15
syscall

jbe_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_jbe
mov rdx, 16
syscall

; -------- Overflow test --------
mov rax, 127
add rax, 1
jo jo_label
jno jno_label

jo_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_jo
mov rdx, 11
syscall

jno_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_jno
mov rdx, 12
syscall

; -------- Sign test --------
mov rax, -5
js js_label
jns jns_label

js_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_js
mov rdx, 10
syscall

jns_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_jns
mov rdx, 11
syscall

; -------- Parity test --------
mov al, 0b00001111
jp jp_label
jnp jnp_label

jp_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_jp
mov rdx, 16
syscall


jnp_label:
mov rax, 1
mov rdi, 1
lea rsi, msg_jnp
mov rdx, 17
syscall

; --- Mixed Instructions---

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

;----- Pop & Push ------

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


; -------- Exit --------
mov rax, 60
mov rdi, 0
syscall
