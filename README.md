# KTU_S3_CA_L1_Assembler
Assembler for Kaunas University of Technology, Semester 3, Computer Architecture, lab assignment 1, natural microprocessor
## Help

### Prerequisites
  - install python 3.5 (add it to PATH)
  - notepad++ is good otion for syntax highlighting in .asm files
    
### [LTU] Realizuotos Operacijos :
  -	jmp address flag - Šuolis į address jei flag yra 0 arba nepaduotas
  -	{label}: - sukuria vietą į kurią gali šokti jmp operacija
  -	mov src dest - Pernešą reikšmė iš src registro į dest registrą
  -	res dest... - Reset‘iną dest (1 ar daugiau) registrus ar loginius elementus (FLAG, CNT, ROM)
  -	shl src - LL1 src registrui
  -	shr src - LR1 src registrui
  -	sal src - AL1 src registrui
  -	sar src - AR1 src registrui
  -	rol src - CL1 src registrui
  -	ror src - CR1 src registrui
  -	add - sudeda L ir R ir išsaugo M į A registrą
  -	xor - xor‘ina L ir R ir išsaugo M į A registrą
  -	not src - apverčia src (L ar R) irišsaugo M į A registrą
  -	inc src - prideda 1 prie src (L ar R) ir išsaugo M į A registrą
  -	dec src - atima 1 iš src (L ar R) arba CNT jei src neduotas ir irišsaugo M į A registrą
  
### assemble
Using console run command:<br>
python assemble.py *source*<br>
egz.: [Windows CMD] python assemble.py code/L1.asm
