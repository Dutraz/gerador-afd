from gramatica.regra import Regra


class Producao:

    def __init__(self, regras: list[Regra] = []):
        self.regras = regras

    def __str__(self):
        return ' | '.join([str(r) for r in self.regras])

    def addRegra(self, regra: Regra):
        self.regras.append(regra)
        return self
