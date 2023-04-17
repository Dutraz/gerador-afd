from src.linguagem.gramatica.simbolo import SimboloNaoTerminal


class Estado:

    def __init__(self, nao_terminais: set[SimboloNaoTerminal] = None, inicial: bool = False, final: bool = False,
                 erro: bool = False):
        self.naoTerminais = nao_terminais or set()
        self.inicial = inicial
        self.final = final
        self.erro = erro
        self.transicoes = dict()

    def __str__(self):
        return f'{",".join(sorted([s.get_caracter() for s in self.naoTerminais]))}'
        # DEBUG ONLY
        # return f'[{", ".join(sorted([s.getCaracter() for s in self.naoTerminais]))}]({str(id(self))[-4:]})'

    def __hash__(self):
        return self.get_caracteres()

    def __eq__(self, other):
        if isinstance(other, Estado):
            # print(self.getCaracteres(), other.getCaracteres())
            return self.get_caracteres() == other.get_caracteres()
        elif isinstance(other, str):
            return self.get_caracteres() == other
        elif isinstance(other, SimboloNaoTerminal):
            return self.get_caracteres() == other.get_caracter()
        else:
            return False

    def get_identificador(self):
        return f'{">" if self.is_inicial() else ""}{str(self)}{"*" if self.is_final() else ""}'

    def add_transicao(self, terminal: str, estado: 'Estado') -> 'Estado':
        self.transicoes[terminal] = estado
        return self

    def get_transicoes(self) -> dict:
        return self.transicoes

    def get_transicao_por(self, terminal: str) -> 'Estado':
        return self.transicoes.get(terminal, None)

    def add_nao_terminais(self, nao_terminal):
        self.naoTerminais.update(nao_terminal)
        return self

    def get_nao_terminais(self):
        return self.naoTerminais

    def get_caracteres(self):
        return ','.join(sorted([e.get_caracter() for e in self.naoTerminais]))

    def set_inicial(self, inicial: bool = True) -> 'Estado':
        self.inicial = inicial
        return self

    def is_inicial(self) -> bool:
        return self.inicial

    def set_final(self, final: bool = True) -> 'Estado':
        self.final = final
        return self

    def is_final(self) -> bool:
        return self.final

    def set_erro(self, erro: bool = True) -> 'Estado':
        self.erro = erro
        return self

    def is_erro(self) -> bool:
        return self.erro

    def is_morto(self, verificados=None) -> bool:
        if verificados is None:
            verificados = []
        if self.is_final():
            return False
        if self in verificados:
            return True

        verificados.append(self)

        for estado in self.transicoes.values():
            if not estado.is_morto(verificados):
                return False

        return True
