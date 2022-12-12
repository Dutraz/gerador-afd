import linguagem.gramatica.simbolo as s


class Regra:

    def __init__(self, simbolos: list = None):
        self.simbolos = simbolos or []

    def __str__(self):
        return ''.join([str(s) for s in self.simbolos])

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return other and str(self) == str(other)

    def addSimbolo(self, simbolo):
        self.simbolos.append(simbolo)
        return self

    def getSimbolos(self):
        return self.simbolos

    def getSimbolosNaoTerminais(self):
        return {
            x for x in self.simbolos if isinstance(x, s.SimboloNaoTerminal)
        }
