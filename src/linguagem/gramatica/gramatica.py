from src.linguagem.gramatica.simbolo import SimboloNaoTerminal, Simbolo


class Gramatica:

    def __init__(self, simbolos: list[SimboloNaoTerminal] = None):
        self.simbolos = simbolos or []

    def __str__(self):
        return '\n'.join([f'{r}::= {r.producao}' for r in self.simbolos])

    def add_simbolo(self, simbolo: SimboloNaoTerminal) -> 'Gramatica':
        self.simbolos.append(simbolo)
        return self

    def get_simbolos(self) -> list[Simbolo]:
        return self.simbolos

    def get_simbolos_nao_terminais(self) -> set[Simbolo]:
        nao_terminais = {
            simbolo for s in self.simbolos for simbolo in s.get_producao().get_simbolos_nao_terminais()
        }
        nao_terminais.update(set([s for s in self.simbolos]))
        return nao_terminais

    def get_tamanho_regras(self) -> list[int]:
        tamanho_regras = []
        for s in self.simbolos:
            tamanho_regras.extend(s.get_tamanho_regras())
        return tamanho_regras
