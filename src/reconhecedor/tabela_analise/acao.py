class Acao:

    def __init__(self, estado):
        self.estado = estado


class Empilhamento(Acao):
    def __str__(self):
        return f'e{self.estado}'


class Reducao(Acao):
    def __str__(self):
        return f'r{self.estado}'


class Salto(Acao):
    def __str__(self):
        return f'{self.estado}'
