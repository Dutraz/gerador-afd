from linguagem.automato.estado import Estado
from linguagem.gramatica.gramatica import Gramatica
from linguagem.gramatica.simbolo import SimboloTerminal, SimboloNaoTerminal, Epsilon
from prettytable import PrettyTable


class Automato:

    def __init__(self, argumento):
        if (argumento is list[Estado]):
            self.estados = argumento
        else:
            self.estados = self.__carregarGramatica(argumento[0])

    def __str__(self):

        terminais = sorted({
            transicoes for e in self.estados for transicoes in e.getTransicoes().keys()
        })

        tab = PrettyTable(list(['-', *terminais]))

        for e in self.estados:
            linha = [str(e)]
            for terminal in terminais:
                transicoes = e.getTransicoesPor(terminal)
                linha.append(
                    f'[{",".join([t.getCaracter() for t in transicoes])}]'
                    if transicoes else '-'
                )
            tab.add_row(linha)
        return str(tab)

    def addEstado(self, estado: Estado):
        self.estados.append(estado)
        return self

    # Transforma uma gramática em um array de estados
    def __carregarGramatica(self, gramatica: Gramatica) -> list[Estado]:

        # Filtra apenas o símbolo inicial da gramática
        simboloInicial = next(filter(
            lambda x: x.isInicial(), gramatica.getSimbolos()
        ))
        simbolosVerificar = {simboloInicial}
        estados = []

        # Enquanto houverem símbolos a verificar, cria um estado para cada símbolo alcançado
        while simbolosVerificar != set():

            simbolo = simbolosVerificar.pop()
            regras = simbolo.getProducao().getRegras()

            estado = Estado(
                {simbolo},
                simbolo.getCaracter() == 'S',  # Estado Inicial
                regras == []  # Estado Final
            )

            for regra in regras:
                estado.setFinal(regra.isFinal())

                # Cria novas transições para cada regra da gramática
                if (not estado.isFinal()):
                    estado.addTransicao(
                        ''.join([
                            s.getCaracter() for s in regra.getSimbolosTerminais()
                        ]), regra.getSimbolosNaoTerminais()
                    )

                    simbolosVerificar.update(
                        regra.getSimbolosNaoTerminais() - {simbolo}
                    )

            estados.append(estado)

        return estados
