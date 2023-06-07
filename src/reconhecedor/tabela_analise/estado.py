class Estado:

    def __init__(self, acoes: dict() = None):
        if acoes is None:
            acoes = dict()
        self.acoes = acoes

    def set_acao(self, simbolo: str, acao):
        self.acoes[simbolo] = acao
        return self

    def get_acao(self, simbolo):
        return self.acoes.get(simbolo)

    def get_acoes(self):
        return self.acoes
