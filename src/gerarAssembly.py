import os
from utils import ler_json

def gerarAssembly():
    data = ler_json()

    instrucoes = []
    
    # Cabeçalho padrão para ARMv7 com suporte a ponto flutuante
    instrucoes.append(".syntax unified")
    instrucoes.append(".arch armv7-a")
    instrucoes.append(".fpu vfp")
    instrucoes.append(".text")
    instrucoes.append(".global main")
    instrucoes.append("main:")
    contador_reg = 0  # Usaremos s0, s1, s2, etc.

    for linha_atual in data:
        for token in linha_atual.get('tokens'):
            tipo = token['type']
            valor = str(token['token'])

            if tipo == 'number':
                # Em ARM, geralmente carregamos a constante num registrador GPR primeiro
                # e depois movemos para o registrador VFP (sX), ou usamos literais
                instrucoes.append(f"\n    // Carrega {valor}")
                instrucoes.append(f"    LDR r0, ={valor}")
                instrucoes.append(f"    VMSR s{contador_reg}, r0")
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
                    
                    # Desempilha 1 registrador (o resultado fica em reg_esq)
                    contador_reg -= 1

    instrucoes.append("    // Fim da execucao")
    instrucoes.append("    BX LR")
        
    # Escrevendo no arquivo .txt/.s
    output_path = os.path.join("results", "assembly.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(instrucoes) + "\n")
            
    return output_path