import re
from linguagem.gramatica.producao import Producao


class Simbolo:

    def __init__(self, caracter: str):
        self.caracter = caracter

    def __str__(self):
        return self.caracter


class SimboloTerminal(Simbolo):

    def __init__(self, caracter: str):
        super().__init__(caracter)


class Epsilon(SimboloTerminal):

    def __init__(self):
        super().__init__('ε')


class SimboloNaoTerminal(Simbolo):

    def __init__(self, texto: str):

        # Verifica se é uma gramática ou caracter
        if ('::=' in texto):
            [self.caracter, self.producao] = self.__decodificarGramatica(texto)
        else:
            super().__init__(texto)
            self.producao = Producao()

        self.inicial = False

    def __str__(self):
        return f'<{self.caracter}>'

    def setInicial(self, inicial: bool = True):
        self.inicial = inicial

    # Decodifica a string da gramática e retorna elementos
    def __decodificarGramatica(self, gramatica: str):

        [simbolo, regras] = gramatica.split('::=')

        simbolo = re.search('<(.*?)>', simbolo).group(1)
        producao = Producao(regras)

        return [simbolo, producao]
