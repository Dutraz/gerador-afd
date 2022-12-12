from linguagem.gramatica.simbolo import SimboloNaoTerminal


class Gramatica:

    def __init__(self, simbolos: list[SimboloNaoTerminal] = None):
        self.simbolos = simbolos or []

    def __str__(self):
        return '\n'.join([f'{r}::= {r.producao}' for r in self.simbolos])

    def addSimbolo(self, simbolo: SimboloNaoTerminal):
        self.simbolos.append(simbolo)
        return self

    def getSimbolos(self):
        return self.simbolos

    def getSimbolosNaoTerminais(self):
        return {
            simbolo for s in self.simbolos for simbolo in s.getProducao().getSimbolosNaoTerminais()
        }
