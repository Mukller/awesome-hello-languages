.data
msg: .ascii "Hello, World!\n"
.text
.global _start
_start:
    mov r7, #4
    mov r0, #1
    ldr r1, =msg
    mov r2, #14
    swi 0
    mov r7, #1
    swi 0
