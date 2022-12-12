from linguagem.gramatica.simbolo import SimboloNaoTerminal, SimboloTerminal
from linguagem.gramatica.gramatica import Gramatica


class Estado:

    def __init__(self, argumento):
        if (isinstance(argumento, SimboloNaoTerminal)):
            self.naoTerminais = [argumento]
        elif (isinstance(argumento, list)):
            self.naoTerminais = argumento

        self.final = False
        self.inicial = False
        self.transicoes = dict()

    def __str__(self):
        return f'{"*" if self.isFinal() else ">" if self.isInicial() else " "}[{", ".join([s.getCaracter() for s in self.naoTerminais])}]'

    def addTransicao(self, terminal, estados: set):
        if (terminal not in self.transicoes):
            self.transicoes[terminal] = set()
        self.transicoes[terminal].update(estados)
        return self

    def addNaoTerminal(self, terminal: SimboloTerminal, estados: list[SimboloNaoTerminal]):
        self.transicoes[terminal] = estados
        return self

    def setFinal(self, final: bool = True):
        self.final = final
        return self

    def setInicial(self, inicial: bool = True):
        self.inicial = inicial
        return self

    def getNaoTerminais(self):
        return self.naoTerminais

    def getTransicoes(self):
        return self.transicoes

    def isFinal(self):
        return self.final

    def isInicial(self):
        return self.inicial
