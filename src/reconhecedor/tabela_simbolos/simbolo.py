class Simbolo:

    def __init__(self, valor_lexico: str, linha: int):
        self.valor_lexico = valor_lexico
        self.linha = linha
        self.estado_final = None
        self.valor_sintatico = None
        self.tipo = None
        self.producao = None
        self.tamanho = None
        self.acoes = None
        self.codigo = None

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

    def get_atributo(self, name):
        return self.__getattribute__(name)

    def set_atributo(self, name, value):
        self.__setattr__(name, value)
        return self

    def set_producao(self, producao: str):
        self.producao = producao
        return self

    def get_producao(self) -> str:
        return self.producao

    def get_tamanho(self) -> int:
        return len(self.producao.split())

    def set_acoes(self, acoes: list[str]):
        self.acoes = acoes
        return self

    def get_acoes(self) -> list[str]:
        return self.acoes
