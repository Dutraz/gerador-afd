class Simbolo:

    def __init__(self, valor_lexico: str, linha: int):
        self.valor_lexico = valor_lexico
        self.linha = linha
        self.estado_final = None
        self.valor_sintatico = None

    def __str__(self):
        return f'[{self.estado_final}]'
        # DEBUG ONLY
        # return f'{self.nome} (linha {self.linha}). {self.estado_final}'

    def get_linha(self):
        return self.linha

    def get_valor_lexico(self):
        return self.valor_lexico

    def set_valor_sintatico(self, valor_sintatico):
        self.valor_sintatico = valor_sintatico
        return self

    def get_valor_sintatico(self):
        return self.valor_sintatico

    def set_estado_final(self, estado_final):
        self.estado_final = estado_final

    def get_estado_final(self):
        return self.estado_final

    def get_caracter_estado_final(self):
        return self.estado_final.get_caracteres()
