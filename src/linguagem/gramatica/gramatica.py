from linguagem.gramatica.simbolo import SimboloNaoTerminal, SimboloTerminal, Epsilon
from linguagem.gramatica.regra import Regra


class Gramatica:

    def __init__(self, argumento=[]):
        if (argumento is SimboloNaoTerminal):
            self.simbolos = list(argumento)
        elif (argumento is list[SimboloNaoTerminal]):
            self.simbolos = argumento
        elif (argumento == []):
            self.simbolos = []

    def __str__(self):
        return '\n'.join([f'{r}::= {r.producao}' for r in self.simbolos])

    def addSimbolo(self, simbolo: SimboloNaoTerminal):
        self.simbolos.append(simbolo)
        return self

    def getSimbolos(self):
        return self.simbolos

    def getSimbolosNaoTerminais(self):
        simbolos = set()
        for simbolo in self.simbolos:
            simbolos.update(simbolo.getProducao().getSimbolosNaoTerminais())
        return simbolos
