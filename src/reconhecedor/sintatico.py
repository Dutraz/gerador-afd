from src.reconhecedor.jsmachines import get_tabela_lr
from src.reconhecedor.tabela_analise.acao import Empilhamento, Reducao, Salto


class AnalisadorSintatico:

    def __init__(self, linguagem, estruturas: str, fita, recarregar_sintatico: bool):
        self.linguagem = linguagem
        self.tabela_analise = get_tabela_lr(
            self.substituir_estados_estruturas(estruturas),
            recarregar_sintatico,
        )
        self.fita = fita

    def substituir_estados_estruturas(self, estruturas):
        for token, simbolo in self.linguagem.automato.get_estados_reconhecedores().items():
            if token:
                estruturas = estruturas.replace(f' {token} ', ' %' + simbolo.get_caracteres() + '% ')
        return estruturas

    def get_tabela_analise(self):
        return self.tabela_analise

    def verificar(self):
        # Pega a tabela de análise
        tabela = self.tabela_analise

        # Faz uma cópia da fita do objeto
        fita = self.fita

        # Inicia a pilha apenas com estado inicial
        pilha = [0]

        # Cria um array com o tamanho das produções
        tamanho_regras = self.linguagem.get_tamanho_regras()
        print(tamanho_regras)

        index_fita = 0

        # Reconhecimento por pilha vazia
        while pilha:
            # Pega o estado do início da fita
            token = fita[index_fita]

            # Pega o estado do topo da pilha
            num_estado = int(pilha[-1])

            # Pega a ação com base no número do estado do topo da pilha
            acao = tabela.get_estado(
                num_estado
            ).get_acao(
                f'%{token.get_estado_final()}%'
            )

            if isinstance(acao, Empilhamento):
                pilha.append(token)
                pilha.append(acao.get_estado())
                index_fita += 1

            elif isinstance(acao, Reducao):
                # pilha.pop(tamanho_regras[acao.get_estado()] * 2)
                print('agora fufu')
                exit()
                pilha.append(token)

            elif isinstance(acao, Salto):
                print('agora fufufufu')
                exit()
                pilha.append(token)
                pilha.append(acao.get_estado())

            else:
                print('aqui deu ruim')
                exit()

            """
            ======= ONLY PRINT =======
            """
            print(
                '$',
                ' '.join([str(c) for c in pilha]),
                ''.join([' ' for _ in range(10 - len(' '.join([str(c) for c in pilha])) + index_fita)]),
                ' '.join([str(f) for f in fita[index_fita:]]),
                '$'
            )
            # exit()
