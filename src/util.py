def gerador_de_tokens():
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    yield from alfabeto
    for char1 in alfabeto:
        for char2 in alfabeto:
            token = char1 + char2
            yield token
