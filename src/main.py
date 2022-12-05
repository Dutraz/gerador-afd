from linguagem.simbolo import Simbolo
from linguagem.regra import Regra
from linguagem.gramatica import Gramatica


def main():
    G = Gramatica()

    # S = Simbolo('S')
    # S.producao.addRegra(Regra([Simbolo('a'), Simbolo('A')])).addRegra(Regra([Simbolo('b'), Simbolo('A')]))
    # G.addSimbolo(S)
    
    # A = Simbolo('A')
    # A.producao.addRegra(Regra([Simbolo('a'), Simbolo('S')])).addRegra(Regra([Simbolo('ε')]))
    # G.addSimbolo(A)

    G.porPalavra('entao')

    print(G)


if __name__ == '__main__':
    main()
