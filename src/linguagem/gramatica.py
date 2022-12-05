from linguagem.simbolo import SimboloNaoTerminal, SimboloTerminal, Epsilon
from linguagem.regra import Regra


class Gramatica:

    def __init__(self, simbolos: list[SimboloNaoTerminal] = []):
        self.simbolos = simbolos

    def __str__(self):
        return '\n'.join([f'{r}::= {r.producao}' for r in self.simbolos])

    def addSimbolo(self, simbolo: SimboloNaoTerminal):
        self.simbolos.append(simbolo)
        return self

    def getSimbolos(self):
        return self.simbolos

    # Preenche as regras da gramática a partir de uma sentença
    def porSentenca(self, sentenca: str):

        # Gera símbolos não terminais em ordem alfabética
        naoTerminal = (
            SimboloNaoTerminal(chr(i)) for i in range(ord('A'), ord('Z'))
        )

        # Armazena os símbolos de controle
        atual = SimboloNaoTerminal('S')
        proximo = None

        # Gera uma nova gramática para cada símbolo da sentença
        for simbolo in sentenca:
            proximo = next(naoTerminal)
            atual.producao.addRegra(Regra([SimboloTerminal(simbolo), proximo]))
            self.addSimbolo(atual)
            atual = proximo

        # Insere a produção final na gramática (contendo apenas epsilon)
        atual.producao.addRegra(Regra([Epsilon()]))
        self.addSimbolo(atual)

        return self
