def lerNumeroDocumento():
    with open('numero.txt', 'r') as arquivo:
        numero = int(arquivo.read())
        return numero

def atualizarNumeroDocumento():
    numero_atual = lerNumeroDocumento()
    novo_numero = numero_atual + 1
    with open('numero.txt', 'w') as arquivo:
        arquivo.write(str(novo_numero))

