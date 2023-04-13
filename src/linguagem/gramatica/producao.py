from src.linguagem.gramatica.regra import Regra


class Producao:

    def __init__(self, regras: list = None):
        self.regras = regras or []

    def __str__(self):
        return ' | '.join([str(r) for r in self.regras])

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return other and str(self) == str(other)

    def add_regra(self, regra: Regra) -> 'Producao':
        self.regras.append(regra)
        return self

    def get_regras(self) -> list[Regra]:
        return self.regras

    def get_simbolos_nao_terminais(self) -> set:
        return {
            simbolo for regra in self.regras for simbolo in regra.get_simbolos_nao_terminais()
        }
