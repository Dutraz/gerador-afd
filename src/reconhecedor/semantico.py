from src.reconhecedor.tabela_simbolos.simbolo import Simbolo
from src.reconhecedor.tabela_simbolos.tabela import Tabela


class AnalisadorSemantico:

    def __init__(self, tabela_simbolos: Tabela):
        self.tabela_simbolos = tabela_simbolos

    def realizar_acoes(self, acoes: list[str], desempilhados: list[Simbolo], reconhecido: Simbolo):
        for acao in acoes:
            self.realizar_acao(acao, desempilhados, reconhecido)

    def realizar_acao(self, acao: str, desempilhados: list[Simbolo], reconhecido: Simbolo):
        if 'addTS' in acao:
            # Separa os atributos
            destino, fonte = [
                {
                    'simbolo': s.split('.')[0].strip(),
                    'atributo': s.split('.')[1].strip(),
                } for s in acao.replace('addTS', '').strip()[1:-1].split(',')
            ]

            print('addTS', fonte, destino)
            print('Desempilhados: ', *[f'{d} ({"" if isinstance(d, str) else d.get_valor_lexico()})' for d in desempilhados])
            print('Reconhecido: ', reconhecido)

            # Encontra quem é o simbolo fonte
            simbolo_fonte = [d for d in desempilhados if d.get_valor_sintatico() == fonte['simbolo']][0]

            # atributo = simbolo_fonte.get_atributo('valor_lexico')
            #
            # # Caso seja uma operação com o símbolo que dá nome à regra reconhecida
            # if reconhecido == destino['simbolo']:
            #     novo_simbolo = Simbolo('', None)
            #     novo_simbolo.set_atributo('valor_lexico', atributo)
            #
            # else:
            #     print('deu aqui')
            #     exit()

