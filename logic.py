import random


def mover(direcao, matriz):  # realiza os movimentos
    if direcao == "w":
        return paraCima(matriz)
    if direcao == "s":
        return paraBaixo(matriz)
    if direcao == "a":
        return paraEsquerda(matriz)
    if direcao == "d":
        return paraDireita(matriz)


def checarStatus(matriz, max_tile=2048):  # verifica se a pessoa chegou nos 2048.
    flat_board = [cell for row in matriz for cell in row]  # 1
    if max_tile in flat_board:  # 2
        return "VENCEU"

    for i in range(4):  # 3
        for j in range(4):
            if j != 3 and matriz[i][j] == matriz[i][j + 1] or \
                    i != 3 and matriz[i][j] == matriz[i + 1][j]:
                return "JOGAR"

    if 0 not in flat_board:  # 4
        return "PERDEU"
    else:
        return "JOGAR"


def colocarDoisOuQuatro(matriz, iter=1):
    for _ in range(iter):
        a = random.randint(0, 3)  # 5
        b = random.randint(0, 3)
        while matriz[a][b] != 0:
            a = random.randint(0, 3)
            b = random.randint(0, 3)

        if sum([cell for row in matriz for cell in row]) in (0, 2):  # 6
            matriz[a][b] = 2
        else:
            matriz[a][b] = random.choice((2, 4))  # 7
    return matriz


def paraEsquerda(matriz):
    contador = 0
    shiftLeft(matriz)  # shift inicial

    # junta as células
    for i in range(4):
        for j in range(3):
            if matriz[i][j] == matriz[i][j + 1] and matriz[i][j] != 0:
                matriz[i][j] *= 2
                matriz[i][j + 1] = 0
                j = 0

    # shift final
    shiftLeft(matriz)
    return matriz


def paraCima(matriz):
    matriz = rotateLeft(matriz)
    matriz = paraEsquerda(matriz)
    matriz = rotateRight(matriz)
    return matriz


# pega a matriz atual, junta as células e 'remove' os 0.
def paraDireita(matriz):
    shiftRight(matriz)
    for i in range(4):
        for j in range(3, 0, -1):
            if matriz[i][j] == matriz[i][j - 1] and matriz[i][j] != 0:
                matriz[i][j] *= 2
                matriz[i][j - 1] = 0
                j = 0

    # shift final
    shiftRight(matriz)
    return matriz


def paraBaixo(matriz):
    matriz = rotateLeft(matriz)
    matriz = paraEsquerda(matriz)
    shiftRight(matriz)
    matriz = rotateRight(matriz)
    return matriz


# remove os 0 quando vc movimentar o nº p/ esquerda
def shiftLeft(matriz):
    for i in range(4):
        nums, count = [], 0
        for j in range(4):
            if matriz[i][j] != 0:
                nums.append(matriz[i][j])
                count += 1
        matriz[i] = nums
        matriz[i].extend([0] * (4 - count))


# remove os 0 quando vc movimentar o nº p/ direita
def shiftRight(matriz):
    for i in range(4):
        nums, count = [], 0
        for j in range(4):
            if matriz[i][j] != 0:
                nums.append(matriz[i][j])
                count += 1
        matriz[i] = [0] * (4 - count)
        matriz[i].extend(nums)


def rotateLeft(matriz):
    b = [[matriz[j][i] for j in range(4)] for i in range(3, -1, -1)]
    return b


def rotateRight(matriz):
    b = rotateLeft(matriz)
    b = rotateLeft(b)
    return rotateLeft(b)
