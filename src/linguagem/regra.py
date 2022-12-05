import linguagem.simbolo as s


class Regra:

    def __init__(self, simbolos=[]):
        self.simbolos = simbolos

    def __str__(self):
        return ''.join([str(s) for s in self.simbolos])

    def addSimbolo(self, simbolo):
        self.simbolos.append(simbolo)
        return self

    # Preenche os símbolos da regra a partir de uma gramática
    def porGramatica(self, gramatica: str):

        self.simbolos = []

        while gramatica:
            simbolo = gramatica[0]

            if simbolo == '<':
                gramatica = gramatica[1:].split('>', 1)
                self.addSimbolo(s.SimboloNaoTerminal(gramatica[0]))
                gramatica = gramatica[1]

            else:
                if simbolo == 'ε':
                    self.addSimbolo(s.Epsilon())
                elif simbolo != ' ':
                    self.addSimbolo(s.SimboloTerminal(simbolo))

                gramatica = gramatica[1:]
        
        return self