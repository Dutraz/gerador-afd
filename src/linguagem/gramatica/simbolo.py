from linguagem.gramatica.producao import Producao


class Simbolo:

    def __init__(self, caracter: str):
        self.caracter = caracter

    def __str__(self):
        return self.caracter

    def getCaracter(self):
        return self.caracter


class SimboloTerminal(Simbolo):

    def __init__(self, caracter: str):
        super().__init__(caracter)

    def __str__(self):
        return self.caracter

    def __hash__(self):
        return hash(self.caracter)


class Epsilon(Simbolo):

    def __init__(self):
        super().__init__('ε')


class SimboloNaoTerminal(Simbolo):

    def __init__(self, texto: str, inicial: bool = False):
        super().__init__(texto)
        self.producao = Producao()
        self.inicial = inicial

    def __str__(self):
        return f'<{self.caracter}>'

    def __hash__(self):
        return hash(self.caracter)

    def __eq__(self, other):
        return self.caracter == other.caracter

    def setCaracter(self, caracter: str):
        self.caracter = caracter

    def setInicial(self, inicial: bool = True):
        self.inicial = inicial

    def getCaracter(self):
        return self.caracter

    def getProducao(self):
        return self.producao

    def isInicial(self):
        return self.inicial
