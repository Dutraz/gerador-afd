from src.linguagem.gramatica.simbolo import SimboloNaoTerminal, SimboloTerminal


class Estado:

    def __init__(self, naoTerminais: set[SimboloNaoTerminal] = None, inicial: bool = False, final: bool = False,
                 erro: bool = False):
        self.naoTerminais = naoTerminais or set()
        self.inicial = inicial
        self.final = final
        self.erro = erro
        self.transicoes = dict()

    def __str__(self):
        return f'[{",".join(sorted([s.getCaracter() for s in self.naoTerminais]))}]'
        # DEBUG ONLY
        # return f'[{", ".join(sorted([s.getCaracter() for s in self.naoTerminais]))}]({str(id(self))[-4:]})'

    def __hash__(self):
        return self.getCaracteres()

    def __eq__(self, other):
        if isinstance(other, Estado):
            # print(self.getCaracteres(), other.getCaracteres())
            return self.getCaracteres() == other.getCaracteres()
        elif isinstance(other, str):
            return self.getCaracteres() == other
        elif isinstance(other, SimboloNaoTerminal):
            return self.getCaracteres() == other.getCaracter()
        else:
            return False

    def getIdentificador(self):
        return f'{">" if self.isInicial() else ""}{str(self)}{"*" if self.isFinal() else ""}'

    def addTransicao(self, terminal: SimboloTerminal, estado: set['Estado']) -> 'Estado':
        self.transicoes[terminal] = estado
        return self

    def getTransicoes(self) -> dict:
        return self.transicoes

    def getTransicaoPor(self, terminal: SimboloTerminal) -> set['Estado']:
        return self.transicoes.get(terminal, None)

    def addNaoTerminais(self, naoTerminal):
        self.naoTerminais.update(naoTerminal)
        return self

    def getNaoTerminais(self):
        return self.naoTerminais

    def getCaracteres(self):
        return ','.join(sorted([e.getCaracter() for e in self.naoTerminais]))

    def setInicial(self, inicial: bool = True) -> 'Estado':
        self.inicial = inicial
        return self

    def isInicial(self) -> bool:
        return self.inicial

    def setFinal(self, final: bool = True) -> 'Estado':
        self.final = final
        return self

    def isFinal(self) -> bool:
        return self.final

    def setErro(self, erro: bool = True) -> 'Estado':
        self.erro = erro
        return self

    def isErro(self) -> bool:
        return self.erro

    def ehMorto(self, verificados=[]) -> bool:
        if self.isFinal():
            return False
        if self in verificados:
            return True

        verificados.append(self)

        for estado in self.transicoes.values():
            if not estado.ehMorto(verificados):
                return False

        return True
