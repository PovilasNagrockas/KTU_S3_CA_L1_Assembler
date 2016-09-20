start:
    mov in B; N1
    mov in C; N2
    nop
multiply:
    jmp next CL
    mov B, L
    add
    mov M, A
next:
    shl B
    shr C
    dec
    jmp multiply CNT
    mov A, L
    end