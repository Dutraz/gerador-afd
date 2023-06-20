from src.reconhecedor.tabela_analise.acao import Acao


class Estado:

    def __init__(self, acoes: dict[Acao] = None):
        if acoes is None:
            acoes = dict()
        self.acoes = acoes

    def set_acao(self, simbolo: str, acao: Acao):
        self.acoes[simbolo] = acao
        return self

    def rm_acao_por(self, simbolo: str):
        del self.acoes[simbolo]
        return self

    def get_acao(self, simbolo) -> Acao:
        return self.acoes.get(simbolo)

    def get_acoes(self) -> dict[Acao]:
        return self.acoes
