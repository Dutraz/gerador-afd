from src.reconhecedor.jsmachines import get_lr_table


class AnalisadorSintatico:

    def __init__(self, linguagem):
        self.linguagem = linguagem
        self.tabela_analise = get_lr_table(
            linguagem.get_gramaticas()[0].get_cfg_string()
        )

    def get_tabela_analise(self):
        return self.tabela_analise
