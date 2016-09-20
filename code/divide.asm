multiply:
    mov in E; N1
    mov in F; N2
    mov E L
	not L
	mov A E
subtract:
	res A
	mov E L
	mov L A
	mov F L
	add
	mov A E
	jmp end AH
	mov B L
	inc L
	mov A B
	jmp subtract
end:
	mov B L
    end