import json
import sys
import time
import bancoDeDados
import pygame
from pygame.locals import *
from copy import deepcopy
from logic import *

pygame.init()
constante = json.load(open("constantes.json", "r"))
screen = pygame.display.set_mode(
    (constante["tamanho"], constante["tamanho"]))
my_font = pygame.font.SysFont(constante["fonte"], constante["tamanho_fonte"], bold=True)
BRANCO = (255, 255, 255)


# Função para checar se ganhou ou perdeu
def checarVitoria(matriz, status, tema, cor_texto, dificuldade, nome, score):
    if status != "JOGAR":
        tamanho = constante["tamanho"]
        s = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)  # se perdeu, uma tela diferente vai aparecer.
        s.fill(constante["cores"][tema]["acabou"])
        screen.blit(s, (0, 0))

        if status == "VENCEU":
            msg = "VOCÊ VENCEU!"
            screen.blit(my_font.render(msg, 1, cor_texto), (120, 180))
            bancoDeDados.inserirResultado(nome, score, dificuldade)

        else:
            msg = "GAME OVER!"
            screen.blit(my_font.render(msg, 1, cor_texto), (140, 180))

        screen.blit(my_font.render("Jogar novamente? (y/n)", 1, cor_texto), (40, 255))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == K_n):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == K_y:  # se 'y' for pressionado, um novo jogo será iniciado.
                    matriz = novoJogo(tema, cor_texto)
                    return matriz, "JOGAR"
    return matriz, status


def novoJogo(tema, cor_texto):  # inicia um novo jogo
    matriz = [[0] * 4 for _ in range(4)]  # limpando a matriz
    display(matriz, tema)

    screen.blit(my_font.render("NOVO JOGO!", 1, cor_texto), (130, 225))
    pygame.display.update()

    time.sleep(1)

    matriz = colocarDoisOuQuatro(matriz, iter=2)
    display(matriz, tema)
    return matriz


def reiniciar(matriz, tema, cor_texto):
    s = pygame.Surface((constante["tamanho"], constante["tamanho"]), pygame.SRCALPHA)
    s.fill(constante["cores"][tema]["acabou"])
    screen.blit(s, (0, 0))

    screen.blit(my_font.render("REINICIAR? (y / n)", 1, cor_texto), (85, 225))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_n):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == K_y:
                matriz = novoJogo(tema, cor_texto)
                return matriz


# Constroi a matriz
def display(matriz, tema):
    screen.fill(tuple(constante["cores"][tema]["fundo"]))
    box = constante["tamanho"] // 4
    preenchimento = constante["preenchimento"]
    for i in range(4):
        for j in range(4):
            cor = tuple(constante["cores"][tema][str(matriz[i][j])])
            pygame.draw.rect(screen, cor, (j * box + preenchimento,
                                           i * box + preenchimento,
                                           box - 2 * preenchimento,
                                           box - 2 * preenchimento), 0)
            if matriz[i][j] != 0:
                if matriz[i][j] in (2, 4):
                    text_colour = tuple(constante["cores"][tema]["escuro"])
                else:
                    text_colour = tuple(constante["cores"][tema]["claro"])
                screen.blit(my_font.render("{:>4}".format(
                    matriz[i][j]), 1, text_colour),
                    (j * box + 2.5 * preenchimento, i * box + 7 * preenchimento))
    pygame.display.update()


def playGame(tema, nome, dificuldade):
    score = 0
    status = "JOGAR"
    if tema == "claro":
        cor_texto = tuple(constante["cores"][tema]["escuro"])
    else:
        cor_texto = BRANCO
    matriz = novoJogo(tema, cor_texto)

    # loop para rodar o jogo
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_q):  # se apertar 'q' o jogo para e fecha
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:  # conferindo a tecla apertada, 'n' fará o jogo reiniciar

                if event.key == pygame.K_n:
                    matriz = reiniciar(matriz, tema, cor_texto)
                if str(event.key) not in constante["keys"]:
                    continue
                else:
                    key = constante["keys"][str(event.key)]
                    score += 1

                new_board = mover(key, deepcopy(matriz))

                if new_board != matriz:
                    matriz = colocarDoisOuQuatro(new_board)
                    display(matriz, tema)

                    status = checarStatus(matriz, dificuldade)
                    (matriz, status) = checarVitoria(matriz, status, tema, cor_texto, dificuldade, nome, score)
