from reconhecedor.tabela.simbolo import Simbolo


class Tabela:
    def __init__(self, simbolos: list[Simbolo]):
        self.simbolos = simbolos

    def __str__(self):
        return '\n'.join([str(simbolo) for simbolo in self.simbolos])