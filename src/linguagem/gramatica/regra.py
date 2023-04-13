import src.linguagem.gramatica.simbolo as s


class Regra:

    def __init__(self, simbolos: list = None):
        self.simbolos = simbolos or []

    def __str__(self):
        return ''.join([str(s) for s in self.simbolos])

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return other and str(self) == str(other)

    def addSimbolo(self, simbolo: 's.Simbolo') -> 'Regra':
        self.simbolos.append(simbolo)
        return self

    def getSimbolos(self) -> list['s.Simbolo']:
        return self.simbolos

    def getSimbolosNaoTerminais(self) -> list['s.SimboloNaoTerminal']:
        return {
            x for x in self.simbolos if isinstance(x, s.SimboloNaoTerminal)
        }

    def getSimbolosTerminais(self) -> list['s.SimboloTerminal']:
        return {
            x for x in self.simbolos if isinstance(x, s.SimboloTerminal)
        }

    def isFinal(self) -> bool:
        return isinstance(self.simbolos[0], s.Epsilon)