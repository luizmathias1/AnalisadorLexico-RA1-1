# Exemplo de fluxo: 4.2 1.0 +
# Lê número 4.2, entra no estado número, recebe o ponto, continua no estado número, recebe o 2, continua no estado número, 
# recebe o espaço, sai do estado número e salva o token "4.2", volta pro estado inicial, recebe o 1, entra no estado número, 
# recebe o ponto, continua no estado número, recebe o 0, continua no estado número, recebe o espaço, sai do estado número e 
# salva o token "1.0", volta pro estado inicial, recebe o +, reconhece como operador e salva o token "+", volta pro estado inicial 
# e termina a leitura da linha.

from utils import addJson

def parseExpressao(linha, line_number=None):
    print(f'\n-- Processing line "{linha}"')
    global balance, qnt_operandos
    balance, qnt_operandos = 0, 0

    tokens = []
    if not isinstance(linha, str): raise TypeError("parseExpressao espera uma string como 'linha'")

    linha = linha.strip()
    if not linha: return tokens

    estado = estadoInicial
    lista = ""
    index = 0
    
    # Caso final, coloca um espaco para forçar o processamento do último token
    while index <= len(linha):
        char = linha[index] if index < len(linha) else ' '
        estado, lista = estado(char, lista, tokens, linha, index)
        index += 1

    return estadoFinal(tokens, linha, line_number)

def estadoInicial(char, lista, tokens, linha, index):
    print('EstadoInicial', char, lista, index)

def estadoNumero(char, lista, tokens, linha, index):
    print('estadoNumero', char, lista, index)

def estadoComando(char, lista, tokens, linha, index):
    print('estadoComando', char, lista, index)
    
def estadoOperador(char, lista, tokens, linha, index):
    print('estadoOperador', char, lista, index)

def estadoParenteses(char, tokens, index):
    print('estadoParenteses', char, index)

def estadoFinal(tokens, linha, line_number=None):
    addJson(linha, tokens, line_number)
    return tokens