import re
from linguagem.producao import Producao


class SimboloNaoTerminal:

    def __init__(self, caracter: str = ''):
        self.caracter = caracter
        self.producao = Producao([])

    def __str__(self):
        return f'<{self.caracter}>'

    # Preenche as regras do símbolo a partir de uma gramática
    def porGramatica(self, gramatica: str):

        [naoTerminal, regras] = gramatica.split('::=')
        
        match = re.search('<(.*?)>', naoTerminal)
        self.caracter = match.group(1)
        self.producao = Producao([]).porGramatica(regras)

        return self


class SimboloTerminal:

    def __init__(self, caracter: str):
        self.caracter = caracter

    def __str__(self):
        return self.caracter


class Epsilon:

    def __init__(self):
        self.caracter = 'ε'

    def __str__(self):
        return 'ε'
