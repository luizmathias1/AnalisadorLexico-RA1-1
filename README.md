# AnalisadorLexico

## Informações acadêmicas

- **Instituição:** Pontifícia Universidade Católica do Paraná.
- **Disciplina:** Construção de Interpretadores.
- **Professor:** Frank Coelho de Alcantara.

## Integrantes do grupo

- Alexandre Faisst — GitHub: @faisstzera
- Bruno Teider — GitHub: @bruno-teider
- Luiz Mathias — GitHub: @luizmathias1
- Rafaela Vecchi — GitHub: @RafaelaVecchi

## Descrição do projeto

AnalisadorLexico é um sistema desenvolvido para analisar, validar e avaliar expressões matemáticas em Notação Polonesa Reversa (RPN), com geração de código assembly para arquitetura ARMv7 DEC1-SOC(v16.1). O sistema implementa:

1. **Análise léxica** com validação de sintaxe e balanceamento de parênteses
2. **Execução de expressões** em pilha (stack) seguindo norma IEEE 754 (64-bit floating point)
3. **Geração de código assembly** compilável para processadores ARM com unidade de ponto flutuante (VFP)
4. **Sistema de memória** que permite armazenar e recuperar resultados em variáveis nomeadas
5. **Comando RES** para acesso a resultados de expressões anteriores
6. **Apresentação formatada** em tabela colorida com suporte a IEEE 754 hexadecimal


## Funcionalidades

### Operações matemáticas suportadas

| Operador | Descrição |
|----------|-----------|
| `+` | Adição |
| `-` | Subtração |
| `*` | Multiplicação |
| `/` | Divisão real |
| `//` | Divisão inteira |
| `%` | Módulo (resto da divisão) |
| `^` | Potenciação |

### Funcionalidades especiais

- **Variáveis de memória**: Armazena resultados com nomes customizados (Ex: `(10.0 MEM)` armazena 10.0 na variável MEM)
- **Comando RES**: Recupera resultado de expressão anterior (Ex: `(1 RES)` recupera resultado da 1ª linha; `(2 RES)` da 2ª linha, etc)
- **Expressões aninhadas**: Suporta parênteses aninhados (Ex: `((2.0 3.0 +) 4.0 *)`)
- **Tratamento de casos extremos**: NaN (operações indefinidas), Inf (overflow), -Inf (underflow)
- **Divisão por zero**: Retorna Inf ou -Inf conforme sinal do dividendo; 0/0 retorna NaN

### Validações implementadas

- Parênteses balanceados
- Quantidade de operandos suficientes para cada operador
- Detecção de caracteres inválidos
- Números malformados (múltiplos pontos, sinais incorretos)
- Índices de RES válidos

## Tecnologias utilizadas

### Linguagem e ambiente

- **Python** 3.6
- Biblioteca padrão apenas (sem dependências externas):
  - `json` - Armazenamento de tokens e resultados
  - `os` - Manipulação de arquivos e diretórios
  - `math` - Operações matemáticas (potência)
  - `struct` - Conversão para IEEE 754 hexadecimal
  - `sys` - Argumentos de linha de comando

### Arquitetura alvo (para assembly gerado)

- **Processador**: ARMv7 DEC1-SOC(v16.1)
- **Coprocessador**: VFP (Vector Floating Point)
- **Padrão**: IEEE 754 double precision (64-bit)

## Estrutura do projeto

```
AnalisadorLexico/
├── src/
│   ├── main.py                    # Ponto de entrada principal
│   ├── parseExpressao.py          # Análise léxica com máquina de estados
│   ├── executarExpressao.py       # Execução RPN em pilha com IEEE 754
│   ├── gerarAssembly.py           # Gerador de código assembly ARM v7 VFP
│   ├── exibirResultados.py        # Formatação e exibição colorida de resultados
│   ├── utils.py                   # Utilitários (leitura de arquivo, JSON, reset)
│   ├── __pycache__/               # Cache Python (gerado automaticamente)
│   └── results/                   # Saída interna
│       ├── assembly.txt           # Código assembly gerado
│       └── tokens.txt             # Tokens e resultados em JSON
├── testes/
│   ├── teste_basico.txt           # Operações simples (adição, variáveis)
│   ├── teste_memoria.txt          # Variáveis de memória e comando RES
│   ├── teste_aninhamento.txt      # Expressões com parênteses aninhados
│   └── expressoes_erro.txt        # Expressões com erros (para validação)
├── results/                       # Saída final (cópias sincronizadas)
│   ├── assembly.txt               # Código assembly final
│   └── tokens.txt                 # JSON final com tokens e resultados
├── README.md                      # Documentação
└── .gitignore                     # Configuração Git (se houver)
```

### Descrição dos arquivos principais

- **main.py**: Orquestra todo o fluxo — lê arquivo de entrada, chama parser, executor, gerador de assembly e exibidor
- **parseExpressao.py**: Implementa máquina de estados léxica que tokeniza expressões RPN
- **executarExpressao.py**: Executa os tokens usando pilha; implementa IEEE 754 com suporte a overflow/underflow
- **gerarAssembly.py**: Traduz tokens para instruções ARM v7 VFP com suporte a displays
- **exibirResultados.py**: Formata saída com cores ANSI, mostra IEEE 754 em hexadecimal, alinha coluna
- **utils.py**: Funções auxiliares para leitura de arquivo, JSON e reset de arquivos de resultado


## Como executar

### Executar com um arquivo de teste

```bash
# Navegar até a pasta do projeto
cd AnalisadorLexico

# Executar com um dos arquivos de teste disponíveis
python src/main.py testes/teste_basico.txt
python src/main.py testes/teste_memoria.txt
python src/main.py testes/teste_aninhamento.txt
```

### O que acontece na execução

1. ✅ **Leitura**: Arquivo de entrada é lido linha por linha
2. ✅ **Parse**: Cada linha é tokenizada e validada
3. ✅ **Execução**: Tokens são executados em pilha (RPN)
4. ✅ **Assembly**: Código ARM é gerado
5. ✅ **Exibição**: Tabela colorida é mostrada no console
6. ✅ **Saída**: Resultados são salvos em `tokens.txt` e `assembly.txt`


## Como testar

### Opção 1: Usar testes inclusos

O projeto fornece 4 arquivos de teste:

```bash
# Teste básico
python src/main.py testes/teste_basico.txt

# Teste com memória
python src/main.py testes/teste_memoria.txt

# Teste com aninhamento 
python src/main.py testes/teste_aninhamento.txt

# Teste de erros 
python src/main.py testes/expressoes_erro.txt
# Esperado: mensagens de erro para expressões inválidas
```

### Opção 2: Criar seu próprio teste

```bash
# Exemplo 1: Minhas operações básicas
(2.0 3.0 +)
(10.0 5.0 -)
(4.0 3.0 *)
(20.0 4.0 /)


python src/main.py test1.txt
# Esperado: 5.0, 5.0, 12.0, 5.0
```

### Validação manual

Após executar testes, você pode verificar:

1. **Console**: Confirme que a tabela de resultados aparece corretamente.
2. **tokens.txt**:  Verifique se o arquivo foi gerado no formato esperado, contendo o array `entries` com as informações de cada expressão processada.  
3. **assembly.txt**: Confirme se o arquivo de saída contém instruções compatíveis com a arquitetura ARMv7.
4. **CPUlator**:  Após a geração do código assembly, recomenda-se abrir o simulador CPUlator (ARMv7 DE1-SoC) para inspeção da execução. Durante essa etapa, verifique:
   - o comportamento do programa no ambiente simulado;
   - os registradores utilizados durante a execução;
   - a interface e os displays.

 Simulador: `https://cpulator.01xz.net/?sys=arm-de1soc&d_audio=48000`


## Formato de entrada e saída

### Formato de entrada (TXT)

Cada linha deve conter **uma expressão RPN dentro de parênteses extenos**:

```
(operando1 operando2 ... operadorN)
```

**Regras:**
- Cada expressão deve estar entre `(` e `)`
- Operandos e operadores separados por espaço
- Números podem ser inteiros ou decimais (ex: `5`, `5.0`, `3.14`)
- Variáveis são nomes em MAIÚSCULAS (ex: `MEM`, `X`, `VALOR`)
- Operadores: `+`, `-`, `*`, `/`, `//`, `%`, `^`
- Comando especial: `RES` (para resultado anterior)

**Exemplos de entrada válida:**

```
(4.0 2.0 +)                      # Resultado: 6.0
(20.0 BALANCO)                   # Armazena 20.0 em BALANCO
((BALANCO) 5.0 +)                # Soma BALANCO + 5.0
(1 RES)                          # Recupera resultado da linha 1
((1 RES) (2 RES) +)              # Soma resultado da linha 1 e 2
```

### Formato de saída: JSON (tokens.txt)

```json
{
  "entries": [
    {
      "line_number": 1,
      "line": "(4.0 2.0 +)",
      "tokens": [
        {"token": "(", "type": "parenthesis", "position": 0},
        {"token": "4.0", "type": "number", "position": 1},
        {"token": "2.0", "type": "number", "position": 5},
        {"token": "+", "type": "operator", "position": 9},
        {"token": ")", "type": "parenthesis", "position": 10}
      ],
      "resultado": 6.0,
      "memoria": ""
    }
  ]
}
```

**Campos:**
- `line_number`: Número da linha no arquivo de entrada
- `line`: Expressão original 
- `tokens`: Array de tokens com tipo e posição
- `resultado`: Resultado da avaliação 
- `memoria`: Nome da variável que armazenou o resultado (vazio se nenhuma)

### Formato de saída: Assembly (assembly.txt)

```asm
.syntax unified
.arch armv7-a
.fpu vfp
.text
.global main
main:
    // Habilitar o VFP
    MRC p15, 0, r0, c1, c0, 2
    ORR r0, r0, #0xF00000
    MCR p15, 0, r0, c1, c0, 2
    ISB
    MOV r0, #0x40000000
    VMSR FPEXC, r0

    // Carrega 4.0
    LDR r0, =num_0
    VLDR s0, [r0]

    // Carrega 2.0
    LDR r0, =num_1
    VLDR s1, [r0]

    // -- Operação: + --
    VADD.F32 s0, s0, s1

    [... mais instruções ...]

.data
num_0: .float 4.0
num_1: .float 2.0

seg7_table:
    [... tabela de 7 segmentos ...]
```

**Características:**
- Sintaxe ARMv7
- Instruções VFP para floating point
- Registradores de ponto flutuante s0-s31
- Suporte a displays HEX com tabela de 7-segmentos
- Estrutura .data com literais numéricos

### Formato de saída: Console (tabela colorida)

```
 Linha | Expressao   | Resultado | IEEE 754 (64-bit) | Memoria
 ------+-------------+-----------+-------------------+--------
 1     | (4.0 2.0 +) |       6.0 |  4018000000000000 | -      
 2     | (1.0 1.0 +) |       2.0 |  4000000000000000 | -      
 ------+-------------+-----------+-------------------+--------
 Total: 2 expressões processadas.
```

**Colunas:**
- **Linha**: Número da linha no arquivo
- **Expressao**: Texto original 
- **Resultado**: Valor calculado (decimais formatados com 1 casa)
- **IEEE 754 (64-bit)**: Representação hexadecimal do float como 64 bits big-endian
- **Memoria**: Nome da variável armazenada (ou `-` se nenhuma)


## Conclusão

O **AnalisadorLexico** é um projeto acadêmico que integra análise léxica, execução interpretada e geração de código assembly. Demonstra compreensão de:

- Máquinas de estados para parsing
- Estruturas de dados (pilha)
- Padrão IEEE 754 para ponto flutuante
- Geração de código intermediário
- Tratamento de erros e validações

O sistema está pronto para processar expressões RPN, exibir resultados com detalhes IEEE 754 e gerar código compilável para arquitetura ARM. 

---

