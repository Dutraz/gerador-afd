from prettytable import PrettyTable

from src.reconhecedor.tabela_analise.estado import Estado


class TabelaAnalise:
    def __init__(self, estados: list[Estado] = None):
        if estados is None:
            estados = []
        self.estados = estados

    def __str__(self):
        simbolos = sorted(
            [*set(s for e in self.estados for s in e.get_acoes().keys())],
            key=lambda x: ((x.index('%') if '%' in x else 100), x.isupper(), len(x), x)
        )

        tabela = PrettyTable(
            [''] + simbolos
        )

        for index, estado in enumerate(self.estados):
            tabela.add_row([index] + [estado.get_acao(s) or '' for s in simbolos])

        return str(tabela)

    def add_estado(self, estado):
        self.estados.append(estado)
        return self

    def get_estados(self):
        return self.estados

    def get_estado(self, estado):
        return self.estados[estado]
