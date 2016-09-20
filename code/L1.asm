mov in D; Enter N1
mov in E; Enter N2
mov in F; Enter N3
; E = N1 - N2
mov E L
not L
inc R
mov D L
add
mov A E
res A D
; F = N3 * N3
mov F B C
multiply:
    jmp next CL
        mov B L
        add
next:
    shl B
    shr C
    dec
    jmp multiply CNT
        mov A F
        res A B
; A = E / F
jmp positive EH
;number is negative
    inc R
    mov A C; CL -> is number negative
    mov E L
    dec L
    mov A E
    jmp subtract
positive:; number is positive
    mov E L
    not L
    mov A E
subtract:
    res A
    mov E L
    mov M A
    mov F L
    add
    mov A E
    jmp end_divide AH
        mov B L
        inc L
        mov A B
        jmp subtract
end_divide:
    jmp end CL; check if number should become negative
        mov B L
        not L
        inc R
        mov A B
end:
    mov B L
    end