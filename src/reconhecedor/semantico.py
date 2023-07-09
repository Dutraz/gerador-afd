class AnalisadorSemantico:

    def __init__(self, tabela_simbolos):
        self.tabela_simbolos = tabela_simbolos

    def realizar_acoes(self, acoes: list[str]):
        for acao in acoes:
            self.realizar_acao(acao)

    @staticmethod
    def realizar_acao(acao):
        if 'addTS' in acao:
            acao = acao.replace('addTS', '').strip()[1:-1].split(',')
            print(acao)
            print('addTS')
            exit()
