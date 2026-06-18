.global _start
.section .data
msg: .ascii "Hello, World!\n"
.section .text
_start:
    movl $4, %eax
    movl $1, %ebx
    movl $msg, %ecx
    movl $14, %edx
    int $0x80
    movl $1, %eax
    xorl %ebx, %ebx
    int $0x80
