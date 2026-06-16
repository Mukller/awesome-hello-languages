    org 100h
    ld de, msg
    ld c, 9
    call 5
    ret
msg: db "Hello, World!$"
