from linguagem.gramatica.simbolo import SimboloNaoTerminal, Simbolo


class Gramatica:

    def __init__(self, simbolos: list[SimboloNaoTerminal] = None):
        self.simbolos = simbolos or []

    def __str__(self):
        return '\n'.join([f'{r}::= {r.producao}' for r in self.simbolos])

    def addSimbolo(self, simbolo: SimboloNaoTerminal) -> 'Gramatica':
        self.simbolos.append(simbolo)
        return self

    def getSimbolos(self) -> Simbolo:
        return self.simbolos

    def getSimbolosNaoTerminais(self) -> set[Simbolo]:
        naoTerminais = {
            simbolo for s in self.simbolos for simbolo in s.getProducao().getSimbolosNaoTerminais()
        }
        naoTerminais.update(set([s for s in self.simbolos]))
        return naoTerminais
