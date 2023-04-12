class Simbolo:

    def __init__(self, nome: str, linha: int):
        self.nome = nome
        self.linha = linha

    def __str__(self):
        return f'{self.nome} (linha {self.linha})'
