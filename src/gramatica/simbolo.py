from gramatica.producao import Producao


class Simbolo:

    def __new__(cls, caracter: str):
        if caracter == 'ε':
            return Episolon(caracter)
        elif caracter.isupper():
            return SimboloNaoTerminal(caracter)
        else:
            return SimboloTerminal(caracter)


class SimboloNaoTerminal:

    def __init__(self, caracter: str):
        self.caracter = caracter
        self.producao = Producao([])

    def __str__(self):
        return f'<{self.caracter}>'


class SimboloTerminal:

    def __init__(self, caracter: str):
        self.caracter = caracter

    def __str__(self):
        return self.caracter


class Episolon:

    def __init__(self):
        self.caracter = 'ε'

    def __str__(self):
        return 'ε'
