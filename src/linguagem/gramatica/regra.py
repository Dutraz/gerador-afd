import src.linguagem.gramatica.simbolo as s


class Regra:

    def __init__(self, simbolos: list = None):
        self.simbolos = simbolos or []

    def __str__(self):
        return ''.join([str(simbolo) for simbolo in self.simbolos])

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return other and str(self) == str(other)

    def add_simbolo(self, simbolo: 's.Simbolo') -> 'Regra':
        self.simbolos.append(simbolo)
        return self

    def get_simbolos(self) -> list['s.Simbolo']:
        return self.simbolos

    def get_simbolos_nao_terminais(self) -> set['s.SimboloNaoTerminal']:
        return {
            x for x in self.simbolos if isinstance(x, s.SimboloNaoTerminal)
        }

    def get_simbolos_terminais(self) -> set['s.SimboloTerminal']:
        return {
            x for x in self.simbolos if isinstance(x, s.SimboloTerminal)
        }

    def is_final(self) -> bool:
        return isinstance(self.simbolos[0], s.Epsilon)
