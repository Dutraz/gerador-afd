from src.reconhecedor.tabela_analise.acao import Empilhamento, Reducao, Salto


class AnalisadorSintatico:

    def __init__(self, linguagem, estruturas: str, fita):
        self.linguagem = linguagem
        print(self.substituir_estados_estruturas(estruturas))
        # self.tabela_analise = get_lr_table(
        #     estruturas
        # )
        self.fita = fita

    def substituir_estados_estruturas(self, estruturas):
        for token, simbolo in self.linguagem.get_regras_reconhecedoras().items():
            if token:
                print(f'substuir {token} por {str(simbolo)}')
                estruturas = estruturas.replace(f' {token} ', ' {{' + simbolo.get_caracter() + '}} ')
                print(estruturas)
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
        subindex_fita = 0

        # Reconhecimento por pilha vazia
        while pilha:
            token = fita[index_fita].get_nome() + '$'
            while token:
                # Pega o valor do topo da pilha
                num_estado = int(pilha[-1])

                # Pega a ação com base no número do estado do topo da pilha
                acao = tabela.get_estado(
                    num_estado
                ).get_acao(
                    token[subindex_fita]
                )

                if isinstance(acao, Empilhamento):
                    pilha.append(token[subindex_fita])
                    pilha.append(acao.get_estado())

                    if subindex_fita < len(token) - 1:
                        subindex_fita += 1
                    else:
                        index_fita += 1
                        subindex_fita = 0

                if isinstance(acao, Reducao):
                    pilha.pop(tamanho_regras[acao.get_estado()] * 2)
                    print('agora fufu')
                    exit()
                    pilha.append(token[subindex_fita])

                if isinstance(acao, Salto):
                    print('agora fufufufu')
                    exit()
                    pilha.append(token[subindex_fita])
                    pilha.append(acao.get_estado())

                """
                ======= ONLY PRINT =======
                """
                print(
                    '$',
                    ' '.join([str(c) for c in pilha]),
                    ''.join(
                        [' ' for _ in range(20 - len(' '.join([str(c) for c in pilha])) + subindex_fita + index_fita)]),
                    ''.join(fita[index_fita].get_nome()[subindex_fita:]),
                    ' '.join([f.get_nome() for f in fita[index_fita + 1:]]),
                )
                # exit()
