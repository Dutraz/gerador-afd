from gramatica.simbolo import SimboloNaoTerminal, SimboloTerminal, Episolon
from gramatica.regra import Regra


class Gramatica:

    def __init__(self, simbolos: list[SimboloNaoTerminal] = []):
        self.simbolos = simbolos

    def __str__(self):
        return '\n'.join([f'{r}::= {r.producao}' for r in self.simbolos])

    def addSimbolo(self, simbolo: SimboloNaoTerminal):
        self.simbolos.append(simbolo)
        return self

    def porPalavra(self, palavra: str):
        # Gera os símbolos não terminais em ordem alfabética
        naoTerminal = (SimboloNaoTerminal(chr(i))
                       for i in range(ord('A'), ord('Z')))

        atual = SimboloNaoTerminal('S')
        proximo = None

        for letra in palavra:
            proximo = next(naoTerminal)
            atual.producao.addRegra(Regra([SimboloTerminal(letra), proximo]))
            self.addSimbolo(atual)
            atual = proximo

        atual.producao.addRegra(Regra([Episolon()]))
        self.addSimbolo(atual)

        return self
