from src.reconhecedor.jsmachines import get_tabela_lr
from src.reconhecedor.tabela_analise.acao import Empilhamento, Reducao, Salto, Aceite


class AnalisadorSintatico:

    def __init__(self, linguagem, sintatico: list[dict], fita, recarregar_sintatico: bool):
        self.linguagem = linguagem
        self.sintatico = sintatico
        self.tabela_analise = get_tabela_lr(
            '\n'.join([f'{e["simbolo"]} -> {e["producao"]}' for e in sintatico]),
            recarregar_sintatico,
        )
        self.fita = fita

    def substituir_por_estados(self):
        reconhecedores = self.linguagem.automato.get_estados_reconhecedores()

        for estado in self.tabela_analise.get_estados():
            nao_terminais = list(estado.get_acoes().keys())
            for nao_terminal in nao_terminais:
                if nao_terminal in reconhecedores:
                    estado.set_acao(
                        f'%{reconhecedores[nao_terminal].get_caracteres()}%',
                        estado.get_acao(nao_terminal)
                    )
                    estado.rm_acao_por(nao_terminal)

    def get_tabela_analise(self):
        return self.tabela_analise

    def verificar(self):
        # Pega a tabela de análise
        tabela = self.tabela_analise

        # Faz uma cópia da fita do objeto
        fita = self.fita

        # Inicia a pilha apenas com estado inicial
        pilha = [0]
        index_fita = 0

        # Reconhecimento por pilha vazia
        while pilha:

            # Pega o estado do topo da pilha
            num_estado = int(pilha[-1])

            # Enquanto houver fita
            if index_fita < len(fita):
                # Pega o estado do início da fita
                token = fita[index_fita]
                terminal = f'%{token.get_estado_final()}%'
            else:
                terminal = '$'

            # Pega a ação com base no número do estado do topo da pilha
            acao = tabela.get_estado(num_estado).get_acao(terminal)

            if isinstance(acao, Empilhamento):
                pilha.append(token)
                pilha.append(acao.get_estado())
                index_fita += 1

            elif isinstance(acao, Reducao):
                # Pega a producao numerada pela reduçãp
                producao = self.sintatico[acao.get_estado()]

                # Desempilha o dobro do tamanho da produção
                for _ in range(producao['tamanho'] * 2):
                    pilha.pop()

                # Pega o número do estado do topo da pilha
                num_estado = int(pilha[-1])

                # Insere o nome da regra no topo da pilha
                pilha.append(producao['simbolo'])

                # Pega a ação resultante dos últimos dois itens da pilha
                acao = tabela.get_estado(
                    num_estado
                ).get_acao(
                    f'{producao["simbolo"]}'
                )

                # Insere a ação resultante dos últimos dois itens da pilha
                pilha.append(acao.get_estado())

            elif isinstance(acao, Salto):
                print('agora fufufufu')
                exit()
                pilha.append(token)
                pilha.append(acao.get_estado())

            elif isinstance(acao, Aceite):
                print('aqui deu boa')
                exit()

            else:
                print('aqui deu ruim')
                exit()

            self.imprime_reconhecimento(pilha, fita, index_fita)

    @staticmethod
    def imprime_reconhecimento(pilha, fita, index_fita):
        escapacamento = 20 - len(
            ' '.join([str(c) for c in pilha])
        ) + len(
            ' '.join([str(f) for f in fita[:index_fita]])
        )

        if index_fita >= len(fita):
            escapacamento = escapacamento - 1

        print(
            '$',
            ' '.join([str(c) for c in pilha]),
            ''.join([' ' for _ in range(escapacamento)]),
            ' '.join([str(f) for f in fita[index_fita:]]),
            '$'
        )
