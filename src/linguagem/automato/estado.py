from linguagem.gramatica.simbolo import SimboloNaoTerminal, SimboloTerminal
from linguagem.gramatica.gramatica import Gramatica


class Estado:

    def __init__(self, naoTerminais: set[SimboloNaoTerminal] = None, inicial: bool = False, final: bool = False):
        self.naoTerminais = naoTerminais or set()
        self.final = inicial
        self.inicial = final
        self.transicoes = dict()

    def __str__(self):
        return f'{">" if self.isInicial() else ""}[{", ".join([s.getCaracter() for s in self.naoTerminais])}]{"*" if self.isFinal() else ""}'

    def __eq__(self, other):
        if isinstance(other, Estado):
            return self.getCaracteres() == other.getCaracteres()
        elif isinstance(other, str):
            return self.getCaracteres() == other
        elif isinstance(other, SimboloNaoTerminal):
            return self.getCaracteres() == other.getCaracter()
        else:
            return False

    def addTransicao(self, terminal: SimboloTerminal, estados: set[SimboloNaoTerminal]) -> 'Estado':
        if (terminal not in self.transicoes):
            self.transicoes[terminal] = set()
        self.transicoes[terminal].update(estados)
        return self

    def getTransicoes(self) -> dict:
        return self.transicoes

    def getTransicoesPor(self, terminal: SimboloTerminal) -> set[SimboloNaoTerminal]:
        return self.transicoes.get(terminal, None)

    def setFinal(self, final: bool = True) -> 'Estado':
        self.final = final
        return self

    def isFinal(self) -> bool:
        return self.final

    def setInicial(self, inicial: bool = True) -> 'Estado':
        self.inicial = inicial
        return self

    def getNaoTerminais(self):
        return self.naoTerminais

    def getCaracteres(self):
        return ','.join(sorted([e.getCaracter() for e in self.naoTerminais]))

    def getTransicoes(self):
        return self.transicoes

    def isFinal(self):
        return self.final

    def isInicial(self):
        return self.inicial
