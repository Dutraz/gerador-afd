class Acao:

    def __init__(self, estado):
        self.estado = int(estado)

    def get_estado(self):
        return self.estado


class Empilhamento(Acao):
    def __str__(self):
        return f'e{self.estado}'


class Reducao(Acao):
    def __str__(self):
        return f'r{self.estado}'


class Salto(Acao):
    def __str__(self):
        return f'{self.estado}'


class Aceite(Acao):
    def __init__(self):
        pass

    def __str__(self):
        return 'acc'
