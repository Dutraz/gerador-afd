from linguagem.gramatica.regra import Regra


class Producao:

    def __init__(self, regras: list = None):
        self.regras = regras or []

    def __str__(self):
        return ' | '.join([str(r) for r in self.regras])

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return other and str(self) == str(other)

    def addRegra(self, regra: Regra):
        self.regras.append(regra)
        return self

    def getRegras(self):
        return self.regras

    def getSimbolosNaoTerminais(self):
        return {
            simbolo for regra in self.regras for simbolo in regra.getSimbolosNaoTerminais()
        }
