import pygame
import random

pygame.init()

WIDTH = 900
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jetpack Insper')
fps = 60
timer = pygame.time.Clock()
fundo = (0, 0, 0)
linhas = [0, WIDTH / 4, 2 * WIDTH / 4, 3 * WIDTH / 4]
velocidade = 2
pause = False

def tela(listalinhas):
    window.fill('black')
    pygame.draw.rect(window, (fundo[0], fundo[1], fundo[2], 50), [0, 0, WIDTH, HEIGHT])
    window.blit(window, (0, 0))
    teto = pygame.draw.rect(window, 'burlywood', [0, 0, WIDTH, 50])
    chao = pygame.draw.rect(window, 'burlywood', [0, HEIGHT - 50, WIDTH, 50])
    for i in range(len(listalinhas)):
        pygame.draw.line(window, 'black', (listalinhas[i], 0), (listalinhas[i], 50), 3)
        pygame.draw.line(window, 'black', (listalinhas[i], HEIGHT - 50), (listalinhas[i], HEIGHT), 3)
        if not pause:
            listalinhas[i] -= velocidade
        if listalinhas[i] < 0:
            listalinhas[i] = WIDTH
    return listalinhas, teto, chao

game = True 
while game:
    timer.tick(fps)
    linhas, teto, chao, = tela(linhas)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    pygame.display.update()
pygame.quit()