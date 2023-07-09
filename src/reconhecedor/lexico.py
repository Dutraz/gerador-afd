from src.reconhecedor.tabela_simbolos.tabela import Tabela


class AnalisadorLexico:

    def __init__(self, linguagem, tokens):
        self.tabela = Tabela()
        self.linguagem = linguagem
        self.carregar_tokens(tokens)

    def get_tabela(self):
        return self.tabela

    def get_str_fita(self):
        return ' '.join([f'[{s.get_caracter_estado_final()}]' for s in self.tabela.simbolos]) + ' $'

    def get_fita(self):
        return self.tabela.simbolos

    def get_erros(self):
        erros = ''
        for s in self.tabela.get_simbolos():
            if s.get_estado_final().is_erro():
                erros += ''.join([
                    f'*** Erro léxico encontrado na linha {s.get_linha()},',
                    f' token não reconhecido: "{s.get_valor_lexico()}".\n'
                ])
        return erros

    def carregar_tokens(self, tokens):

        automato = self.linguagem.get_automato()
        estado_erro = automato.get_estado_erro()

        for token in tokens:
            estado_atual = automato.get_estado_inicial()
            for caracter in token.valor_lexico:

                if caracter not in estado_atual.get_transicoes():
                    estado_atual = estado_erro
                    break

                estado_atual = estado_atual.get_transicao_por(caracter)

                if estado_atual.is_erro():
                    break

            # Caso o último estado do token não seja final (token incompleto)
            if not estado_atual.is_final():
                estado_atual = estado_erro

            token.set_estado_final(estado_atual)
            token.set_valor_sintatico(estado_atual.get_token_reconhecido())
            self.tabela.add_simbolo(token)
