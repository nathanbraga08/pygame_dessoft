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
font = pygame.font.SysFont(None, 32)
gravidade = 0
v_y = 0
init_y = HEIGHT - 150
boneco_y = init_y
boost = False

#criando cenário
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

def draw_pause():
    pygame.draw.rect(window, (128, 128, 128, 150), [0, 0, WIDTH, HEIGHT])
    restart_btn = pygame.draw.rect(window, 'white', [200, 220, 280, 50], 0, 10)
    window.blit(font.render('Continuar', True, 'black'), (220, 230))
    quit_btn = pygame.draw.rect(window, 'white', [520, 220, 280, 50], 0, 10)
    window.blit(font.render('Sair', True, 'black'), (540, 230))
    return restart_btn, quit_btn

#criando avatar
def desenha_avatar():
    player = pygame.rect.Rect((120, boneco_y + 10), (25,60))
    #pygame.draw.rect(window, 'green', player, 5)

    if boneco_y < init_y or pause:
        if boost:
            pygame.draw.ellipse(window, 'red', [100, boneco_y + 50, 20, 30])
            pygame.draw.ellipse(window, 'orange', [105, boneco_y + 50, 10, 30])
            pygame.draw.ellipse(window, 'yellow', [110, boneco_y + 50, 5, 30])
        pygame.draw.rect(window, 'yellow', [128, boneco_y + 60, 10, 20], 0, 3)
        pygame.draw.rect(window, 'orange', [130, boneco_y + 60, 10, 20], 0, 3)
    else:
        if contador < 10:
            pygame.draw.line(window, 'yellow', (128, boneco_y + 60), (140, boneco_y + 80), 10)
            pygame.draw.line(window, 'orange', (130, boneco_y + 60), (120, boneco_y + 80), 10)
        elif 10 <= contador < 20:
            pygame.draw.rect(window, 'yellow', [128, boneco_y + 60, 10, 20], 0, 3)
            pygame.draw.rect(window, 'orange', [130, boneco_y + 60, 10, 20], 0, 3)
        elif 20 <= contador < 30:
            pygame.draw.line(window, 'yellow', (128, boneco_y + 60), (120, boneco_y + 80), 10)
            pygame.draw.line(window, 'orange', (130, boneco_y + 60), (140, boneco_y + 80), 10)
        else:
            pygame.draw.rect(window, 'yellow', [128, boneco_y + 60, 10, 20], 0, 3)
            pygame.draw.rect(window, 'orange', [130, boneco_y + 60, 10, 20], 0, 3)

    pygame.draw.rect(window, 'white', [100, boneco_y + 20, 20, 30], 0, 5)
    pygame.draw.ellipse(window, 'orange', [120, boneco_y + 20, 20, 50])
    pygame.draw.circle(window, 'orange', (135, boneco_y + 15), 10)
    pygame.draw.circle(window, 'black', (138, boneco_y + 12), 3)
    return player

game = True 
while game:
    timer.tick(fps)
    if contador < 40:
        contador += 1
    else:
        contador = 0

    linhas, teto, chao, = tela(linhas)

    avatar = desenha_avatar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not pause:
                boost = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    boost = False
    if not pause:
            if boost:
                v_y -= gravidade
            else:
                v_y += gravidade
            boneco_y += v_y

    pygame.display.update()
pygame.quit()