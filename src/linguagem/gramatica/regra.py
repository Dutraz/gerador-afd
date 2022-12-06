import linguagem.gramatica.simbolo as s


class Regra:

    def __init__(self, argumento, simbolos = list()):
        if (argumento is s.Simbolo):
            self.simbolos = list(argumento)
        elif (isinstance(argumento, list)):
            self.simbolos = argumento
        elif (isinstance(argumento, str)):
            self.simbolos = self.__decodificarGramatica(argumento, simbolos)

    def __str__(self):
        return ''.join([str(s) for s in self.simbolos])

    def addSimbolo(self, simbolo):
        self.simbolos.append(simbolo)
        return self

    def getSimbolos(self):
        return self.simbolos

    def getSimbolosNaoTerminais(self):
        return (
            x for x in self.simbolos if isinstance(x, s.SimboloNaoTerminal)
        )

    # Decodifica a string da gramática e retorna elementos
    def __decodificarGramatica(self, gramatica: str, simbolosGramatica: list):

        simbolos = []

        while gramatica:
            simbolo = gramatica[0]

            if simbolo == '<':
                gramatica = gramatica[1:].split('>', 1)
                simbolos.append(s.SimboloNaoTerminal(gramatica[0]))
                gramatica = gramatica[1]

            else:
                if simbolo == 'ε':
                    simbolos.append(s.Epsilon())
                elif simbolo != ' ':
                    simbolos.append(s.SimboloTerminal(simbolo))

                gramatica = gramatica[1:]

        return simbolos
