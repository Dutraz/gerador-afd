class Simbolo:

    def __init__(self, nome: str, linha: int):
        self.nome = nome
        self.linha = linha
        self.estado_final = None

    def __str__(self):
        return f'{self.nome} (linha {self.linha}). {self.estado_final}'

    def get_linha(self):
        return self.linha

    def get_nome(self):
        return self.nome

    def set_estado_final(self, estado_final):
        self.estado_final = estado_final

    def get_estado_final(self):
        return self.estado_final

    def get_caracter_estado_final(self):
        return self.estado_final.get_caracteres()
