org 100h
    mov ah, 9
    mov dx, msg
    int 21h
    ret
msg db "Hello, World!$"
