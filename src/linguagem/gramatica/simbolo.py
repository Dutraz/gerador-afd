from linguagem.gramatica.producao import Producao


class Simbolo:

    def __init__(self, caracter: str):
        self.caracter = caracter

    def __str__(self):
        return self.caracter

    def __hash__(self):
        return hash(self.caracter)

    def getCaracter(self):
        return self.caracter


class SimboloTerminal(Simbolo):

    def __init__(self, caracter: str):
        super().__init__(caracter)


class Epsilon(Simbolo):

    def __init__(self):
        super().__init__('ε')


class SimboloNaoTerminal(Simbolo):

    def __init__(self, caracter: str, inicial: bool = False):
        super().__init__(caracter)
        self.producao = Producao()
        self.inicial = inicial

    def __str__(self):
        return f'<{self.caracter}>'

    def __hash__(self):
        return hash((self.caracter, self.producao))

    def __eq__(self, other):
        return other and self.caracter == other.caracter and self.producao == other.producao

    def setCaracter(self, caracter: str):
        self.caracter = caracter

    def getCaracter(self):
        return self.caracter

    def setInicial(self, inicial: bool = True):
        self.inicial = inicial

    def isInicial(self):
        return self.inicial

    def getProducao(self):
        return self.producao
