from linguagem.gramatica.simbolo import SimboloNaoTerminal, SimboloTerminal, Epsilon
from linguagem.gramatica.regra import Regra


class Gramatica:

    def __init__(self, argumento=[]):
        if (argumento is SimboloNaoTerminal):
            self.simbolos = list(argumento)
        elif (argumento is list[SimboloNaoTerminal]):
            self.simbolos = argumento
        elif (isinstance(argumento, str)):
            self.simbolos = self.__decodificarSentenca(argumento)
        elif (argumento == []):
            self.simbolos = []

    def __str__(self):
        return '\n'.join([f'{r}::= {r.producao}' for r in self.simbolos])

    def addSimbolo(self, simbolo: SimboloNaoTerminal):
        self.simbolos.append(simbolo)
        return self

    def getSimbolos(self):
        return self.simbolos

    # Decodifica a string da gramática e retorna elementos
    def __decodificarSentenca(self, sentenca: str):

        # Gera símbolos não terminais em ordem alfabética
        naoTerminal = (
            SimboloNaoTerminal(chr(i)) for i in range(ord('A'), ord('Z'))
        )

        # Armazena os símbolos de controle
        atual = SimboloNaoTerminal('S')
        proximo = None
        simbolos = []

        # Gera uma nova gramática para cada símbolo da sentença
        for simbolo in sentenca:
            proximo = next(naoTerminal)
            atual.producao.addRegra(Regra([SimboloTerminal(simbolo), proximo]))
            simbolos.append(atual)
            atual = proximo

        # Insere a produção final na gramática (contendo apenas epsilon)
        atual.producao.addRegra(Regra([Epsilon()]))
        simbolos.append(atual)

        return simbolos
