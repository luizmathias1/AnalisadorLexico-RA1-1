import json
import os
import math
from utils import ler_json

def calcularIEEE754(a, b, operador):
    #Regra para norma IEEE 754(float 64 bits):
    
    try:
        if operador == "+": return a + b
        if operador == "-": return a - b
        if operador == "*": return a * b
        if operador == "/":
            if b == 0.0:
                if a == 0.0: return float('nan')
                return float('inf') if a > 0 else float('-inf')
            return a / b
        if operador == "//": return a // b
        if operador == "%": return a % b
        if operador == "^": return math.pow(a, b)
    except OverflowError:
        # Se o número for grande demais para 64 bits, retorna Infinito
        return float('inf')
    except ZeroDivisionError:
        return float('inf')
    return 0.0