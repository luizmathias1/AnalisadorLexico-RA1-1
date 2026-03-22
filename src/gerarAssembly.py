import os
from utils import ler_json

def gerarAssembly():
    data = ler_json()

    instrucoes = []
    
    # Cabeçalho pro codigo
    instrucoes.append(".syntax unified")
    instrucoes.append(".arch armv7-a")
    instrucoes.append(".fpu vfp")
    instrucoes.append(".text")
    instrucoes.append(".global main")
    instrucoes.append("main:")
    
    # Habilitar o VFP (funcionar float)
    instrucoes.append("\n    // Habilitar o VFP")
    instrucoes.append("    MRC p15, 0, r0, c1, c0, 2")
    instrucoes.append("    ORR r0, r0, #0xF00000")
    instrucoes.append("    MCR p15, 0, r0, c1, c0, 2")
    instrucoes.append("    ISB\n")
    instrucoes.append("    MOV r0, #0x40000000")
    instrucoes.append("    VMSR FPEXC, r0")

    contador_reg = 0  # s0, s1, s2, etc.
    literais = []

    for linha_atual in data:
        for token in linha_atual.get('tokens'):
            tipo = token['type']
            valor = str(token['token'])

            if tipo == 'number':
                # Puxamos os valores de .data
                label = f"num_{len(literais)}"
                literais.append((label, valor))
                
                instrucoes.append(f"\n    // Carrega {valor}")
                instrucoes.append(f"    LDR r0, ={label}")
                instrucoes.append(f"    VLDR s{contador_reg}, [r0]")
                contador_reg += 1
                
            elif tipo == 'operator':
                if contador_reg >= 2:
                    reg_dir = contador_reg - 1
                    reg_esq = contador_reg - 2
                    
                    instrucoes.append(f"\n    // Operação: {valor}")
                    if valor == '+':
                        instrucoes.append(f"    VADD.F32 s{reg_esq}, s{reg_esq}, s{reg_dir}")
                    elif valor == '-':
                        instrucoes.append(f"    VSUB.F32 s{reg_esq}, s{reg_esq}, s{reg_dir}")
                    elif valor == '*':
                        instrucoes.append(f"    VMUL.F32 s{reg_esq}, s{reg_esq}, s{reg_dir}")
                    elif valor == '/':
                        instrucoes.append(f"    VDIV.F32 s{reg_esq}, s{reg_esq}, s{reg_dir}")
                    elif valor == '//':
                        instrucoes.append(f"    VDIV.F32 s{reg_esq}, s{reg_esq}, s{reg_dir}")
                        instrucoes.append(f"    VCVT.S32.F32 s{reg_esq}, s{reg_esq}") # Trunca para int
                        instrucoes.append(f"    VCVT.F32.S32 s{reg_esq}, s{reg_esq}") # Volta para float
                    elif valor == '%':
                        # Modulo Float: A - (int(A / B) * B)
                        s_tmp = contador_reg
                        instrucoes.append(f"    VDIV.F32 s{s_tmp}, s{reg_esq}, s{reg_dir}")
                        instrucoes.append(f"    VCVT.S32.F32 s{s_tmp}, s{s_tmp}") # Trunca para int
                        instrucoes.append(f"    VCVT.F32.S32 s{s_tmp}, s{s_tmp}") # Volta para float
                        instrucoes.append(f"    VMUL.F32 s{s_tmp}, s{s_tmp}, s{reg_dir}")
                        instrucoes.append(f"    VSUB.F32 s{reg_esq}, s{reg_esq}, s{s_tmp}")
                    elif valor == '^':
                        # Potência (assumindo expoente como inteiro >= 0 para simplificar a repetição)
                        lbl = f"pow_{len(literais)}"
                        s_tmp = contador_reg
                        label_1 = f"num_{len(literais)}"
                        literais.append((label_1, "1.0"))
                        
                        instrucoes.append(f"    VCVT.S32.F32 s{s_tmp}, s{reg_dir}") # converte expoente para int
                        instrucoes.append(f"    VMOV r1, s{s_tmp}")                 # r1 = contador do loop (expoente)
                        instrucoes.append(f"    LDR r2, ={label_1}")
                        instrucoes.append(f"    VLDR s{s_tmp}, [r2]")               # s_tmp = 1.0 (acumulador do resultado)
                        instrucoes.append(f"{lbl}_loop:")
                        instrucoes.append(f"    CMP r1, #0")
                        instrucoes.append(f"    BLE {lbl}_end")
                        instrucoes.append(f"    VMUL.F32 s{s_tmp}, s{s_tmp}, s{reg_esq}")
                        instrucoes.append(f"    SUB r1, r1, #1")
                        instrucoes.append(f"    B {lbl}_loop")
                        instrucoes.append(f"{lbl}_end:")
                        instrucoes.append(f"    VMOV.F32 s{reg_esq}, s{s_tmp}")    # devolve o resultado para reg_esq
                    
                    # Desempilha 1 registrador (o resultado fica em reg_esq)
                    contador_reg -= 1

                    instrucoes.append(f"\n    // Converte float para inteiro")
                    instrucoes.append(f"    VCVT.S32.F32 s{reg_esq}, s{reg_esq}")
                    instrucoes.append(f"    VMOV r0, s{reg_esq}")          # r0 = resultado inteiro

                    instrucoes.append(f"\n    // Lookup 7 segmentos: r0 = seg7_table[r0]")
                    instrucoes.append(f"    LDR r1, =seg7_table")
                    instrucoes.append(f"    LDR r0, [r1, r0, LSL #2]")     # cada entry ocupa 4 bytes

                    instrucoes.append(f"\n    // Escreve no HEX0 (display mais à direita)")
                    instrucoes.append(f"    LDR r1, =0xFF200020")
                    instrucoes.append(f"    STR r0, [r1]")

            elif tipo == 'parenthesis':
                # Parênteses não geram código
                pass

    instrucoes.append("    // Fim da execucao")
    instrucoes.append("    BX LR")
    
    # Adicionando os valores literais em floats num segmento .data para asswmbly ler
    if literais:
        instrucoes.append("\n.data")
        for label, val in literais:
            instrucoes.append(f"{label}:")
            instrucoes.append(f"    .float {val}")
    
    instrucoes.append("\nseg7_table:")
    instrucoes.append("    .word 0x3F  // 0")
    instrucoes.append("    .word 0x06  // 1")
    instrucoes.append("    .word 0x5B  // 2")
    instrucoes.append("    .word 0x4F  // 3")
    instrucoes.append("    .word 0x66  // 4")
    instrucoes.append("    .word 0x6D  // 5")
    instrucoes.append("    .word 0x7D  // 6")
    instrucoes.append("    .word 0x07  // 7")
    instrucoes.append("    .word 0x7F  // 8")
    instrucoes.append("    .word 0x6F  // 9")
        
    # Escrevendo no arquivo txt
    output_path = os.path.join("results", "assembly.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(instrucoes) + "\n")
            
    return output_path