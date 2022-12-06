from linguagem.gramatica.regra import Regra


class Producao:

    def __init__(self, argumento=[]):
        if (argumento is Regra):
            self.regras = list(argumento)
        elif (argumento is list[Regra]):
            self.regras = argumento
        elif (argumento == []):
            self.regras = []

    def __str__(self):
        return ' | '.join([str(r) for r in self.regras])

    def addRegra(self, regra: Regra):
        self.regras.append(regra)
        return self

    def getRegras(self):
        return self.regras

    def getSimbolosNaoTerminais(self):
        simbolos = set()
        for regra in self.regras:
            simbolos.update(regra.getSimbolosNaoTerminais())
        return simbolos
