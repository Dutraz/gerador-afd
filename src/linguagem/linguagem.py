from linguagem.automato.automato import Automato
from linguagem.gramatica.gramatica import Gramatica
from linguagem.gramatica.simbolo import SimboloNaoTerminal


class Linguagem:

    def __init__(self):
        self.gramaticas = []
        self.automato = []

    def __str__(self):
        return '\n\n'.join([str(g) for g in self.gramaticas])

    def setGramaticas(self, gramaticas: list[Gramatica]) -> 'Linguagem':
        self.gramaticas = gramaticas
        return self

    def addGramatica(self, gramatica: Gramatica) -> 'Linguagem':
        self.gramaticas.append(gramatica)
        return self

    def gerarAutomato(self, gramaticas: list[Gramatica] = None) -> 'Linguagem':
        self.automato = Automato(gramaticas or self.gramaticas)
        return self

    def getAutomato(self) -> Automato:
        return self.automato

    def unificarGramaticas(self) -> Gramatica:
        # Cria uma nova gramática inicializada por um novo <S> inicial
        simboloInicial = SimboloNaoTerminal('S', True)
        g = Gramatica()
        g.addSimbolo(simboloInicial)

        # Unifica todas as gramáticas compartilhando apenas o <S>
        for gramatica in self.gramaticas:
            for simbolo in gramatica.getSimbolos():
                # Se é simbolo inicial, soma às gramáticas de S
                if (simbolo.isInicial()):
                    for regra in simbolo.getProducao().getRegras():
                        simboloInicial.getProducao().addRegra(regra)
                else:
                    # Se não é simbolo inicial, procura por símbolo ainda não utilizado
                    while (simbolo.getCaracter() in [s.getCaracter() for s in g.getSimbolos()]):
                        simbolo.setCaracter(
                            chr(ord(simbolo.getCaracter()) + 1)
                        )
                    g.addSimbolo(simbolo)

                # Substituindo o S nas regras pelo novo S instanciado
                for regra in simbolo.getProducao().getRegras():
                    for i, s in enumerate(regra.getSimbolos()):
                        if isinstance(s, SimboloNaoTerminal) and s.isInicial():
                            regra.getSimbolos()[i] = simboloInicial
        return g
