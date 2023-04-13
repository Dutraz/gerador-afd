from src.linguagem.gramatica.producao import Producao


class Simbolo:

    def __init__(self, caracter: str):
        self.caracter = caracter

    def __str__(self):
        return self.caracter

    def __hash__(self):
        return hash(self.caracter)

    def get_caracter(self) -> str:
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
        # Debug only
        # return f'<{self.caracter}({str(id(self))[-4:]})>'

    def __hash__(self):
        return hash((self.caracter, self.producao))

    def __eq__(self, other):
        if isinstance(other, Simbolo):
            return self.caracter == other.caracter
        elif isinstance(other, str):
            return self.caracter == other
        else:
            return False

    def set_caracter(self, caracter: str) -> 'SimboloNaoTerminal':
        self.caracter = caracter
        return self

    def set_inicial(self, inicial: bool = True) -> 'SimboloNaoTerminal':
        self.inicial = inicial
        return self

    def is_inicial(self) -> bool:
        return self.inicial

    def get_producao(self) -> 'Producao':
        return self.producao
