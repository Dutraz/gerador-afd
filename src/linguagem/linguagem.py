from src.linguagem.automato.automato import Automato
from src.linguagem.gramatica.gramatica import Gramatica
from src.linguagem.gramatica.simbolo import SimboloNaoTerminal, SimboloTerminal, Epsilon


class Linguagem:

    def __init__(self):
        self.gramaticas = []
        self.automato = None

    def __str__(self):
        return '\n\n'.join([str(g) for g in self.gramaticas])

    def set_gramaticas(self, gramaticas: list[Gramatica]) -> 'Linguagem':
        self.gramaticas = gramaticas
        return self

    def add_gramatica(self, gramatica: Gramatica) -> 'Linguagem':
        self.gramaticas.append(gramatica)
        return self

    def gerar_automato(self, gramaticas: list[Gramatica] = None) -> 'Linguagem':
        self.automato = Automato(gramaticas or self.gramaticas)
        return self

    def get_automato(self) -> Automato:
        return self.automato

    def unificar_gramaticas(self) -> Gramatica:
        # Cria uma gramática inicializada por um novo <S> inicial
        simbolo_inicial = SimboloNaoTerminal('S', True)
        g = Gramatica()
        g.add_simbolo(simbolo_inicial)

        # Unifica todas as gramáticas compartilhando apenas o <S>
        for gramatica in self.gramaticas:
            for simbolo in gramatica.get_simbolos():
                # Se é tabela inicial, soma às gramáticas de S
                if simbolo.is_inicial():
                    for regra in simbolo.get_producao().get_regras():
                        simbolo_inicial.get_producao().add_regra(regra)
                else:
                    # Se não é tabela inicial, procura por símbolo ainda não utilizado
                    while simbolo.get_caracter() in [s.get_caracter() for s in g.get_simbolos()]:
                        simbolo.set_caracter(
                            chr(ord(simbolo.get_caracter()) + 1)
                        )
                    g.add_simbolo(simbolo)

                # Substituindo o S nas regras pelo novo S instanciado
                for regra in simbolo.get_producao().get_regras():
                    for i, s in enumerate(regra.get_simbolos()):
                        if isinstance(s, SimboloNaoTerminal) and s.is_inicial():
                            regra.get_simbolos()[i] = simbolo_inicial
        return g

    def remover_epsilon_transicoes(self):
        alteracao = True

        gramaticas = self.gramaticas

        while alteracao:
            alteracao = False
            for gramatica in gramaticas:
                for simbolo in gramatica.get_simbolos():
                    for regra in simbolo.get_producao().get_regras():
                        if True not in [isinstance(s, (SimboloTerminal, Epsilon)) for s in regra.get_simbolos()]:
                            alteracao = True
                            for regra_mover in regra.get_simbolos()[0].get_producao().get_regras():
                                simbolo.get_producao().add_regra(regra_mover)
                            simbolo.get_producao().get_regras().remove(regra)

        return gramaticas
