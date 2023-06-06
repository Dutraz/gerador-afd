from src.reconhecedor.jsmachines import get_lr_table
from src.reconhecedor.tabela.tabela import Tabela


class AnalisadorSintatico:

    def __init__(self, linguagem):
        self.tabela = Tabela()
        self.linguagem = linguagem
        self.tabela = get_lr_table(
            linguagem.get_gramaticas()[0].get_cfg_string()
        )

    def get_tabela(self):
        pass

    def get_fita(self):
        pass

    def get_erros(self):
        pass

    def carregar_tokens(self, tokens):
        pass
