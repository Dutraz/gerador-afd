def salvarCodigoIntermediario(codigo):
    with open('./arquivos/codigo_intermediario.txt', 'w') as file:
        for line in codigo.split("\\n"):
            file.write(f'{line}\n')
