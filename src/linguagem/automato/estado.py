from linguagem.gramatica.simbolo import SimboloNaoTerminal, SimboloTerminal
from linguagem.gramatica.gramatica import Gramatica


class Estado:

    def __init__(self, argumento):
        if (isinstance(argumento, str)):
            self.naoTerminais = set(argumento)
        elif (isinstance(argumento, set)):
            self.naoTerminais = argumento

        self.transicoes = dict()

    def __str__(self):
        return ', '.join(self.naoTerminais)

    def addTransicao(self, terminal, estados: set):
        if (terminal not in self.transicoes):
            self.transicoes[terminal] = set()
        self.transicoes[terminal].update(estados)
        return self

    def addNaoTerminal(self, terminal: SimboloTerminal, estados: list[SimboloNaoTerminal]):
        self.transicoes[terminal] = estados
        return self

    def getTransicoes(self):
        return self.transicoes
