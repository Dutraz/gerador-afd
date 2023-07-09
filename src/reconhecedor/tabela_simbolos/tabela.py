from prettytable import PrettyTable


class Tabela:
    def __init__(self, simbolos=None):
        if simbolos is None:
            simbolos = []
        self.simbolos = simbolos

    def __str__(self):
        tabela = PrettyTable(list(['ESTADO', 'LÉXICO', 'SINTÁTICO', 'LINHA']))
        for s in self.simbolos:
            tabela.add_row(
                [f'[{s.get_caracter_estado_final()}]' if s.get_estado_final() else '', s.get_valor_lexico(),
                 s.get_valor_sintatico(), s.get_linha()]
            )
        return str(tabela)

    def add_simbolo(self, simbolo):
        self.simbolos.append(simbolo)
        return self

    def get_simbolos(self):
        return self.simbolos
