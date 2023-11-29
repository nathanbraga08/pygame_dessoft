import pygame
import random

pygame.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jetpack Insper')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
fundo = (0,0,0)
linhas = [0, WIDTH / 4, 2 * WIDTH / 4, 3 * WIDTH / 4]
velocidade = 3
pause = False
init_y = HEIGHT - 130
boneco_y = init_y
boost = True
contador = 0
v_y = 0 
gravidade = 0.4
atualiza_laser = True
laser = []
distancia = 0
pontuacao = 0 
reviver = False
vida = 3

# Carrega os sons do jogo
pygame.mixer.music.load('efeito-sonoro-hd.ogg')
pygame.mixer.music.set_volume(0.4)

def tela(listalinhas,listalaser):
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
            listalaser[0][0] -= velocidade
            listalaser[1][0] -= velocidade
        if listalinhas[i] < 0:
            listalinhas[i] = WIDTH
    linha_do_laser = pygame.draw.line(window, 'red', (listalaser[0][0],listalaser[0][1]),(listalaser[1][0],listalaser[1][1]), 10)
    window.blit(font.render(f'distancia percorrida: {int(distancia)} m', True, 'white'), (10,10))
    window.blit(font.render(f'recorde: {int(pontuacao)} m', True, 'white'), (10,70))
    return listalinhas, teto, chao, listalaser, linha_do_laser

def desenha_avatar():
    player = pygame.rect.Rect((120, boneco_y + 10), (25,60))

    if boneco_y < init_y or pause:
        if boost:
            pygame.draw.ellipse(window, 'red', [100, boneco_y + 50, 20, 30])
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

def vercolisao():
    cool = [False, False]
    restart = False
    vida = 3
    if avatar.colliderect(chao_plat):
        cool[0] = True
    elif avatar.colliderect(teto_plat):
        cool[1] = True
    if linha_do_laser.colliderect(avatar):
        restart = True
        vida -= 1
    return cool, restart, vida

def laser_gerado():
    tipo_de_laser = random.randint(0,1)
    offset = random.randint(10,300)
    match tipo_de_laser:
        case 0:
            larg_laser = random.randint(100, 300)
            laser_y = random.randint(100, HEIGHT - 100)
            atualiza_laser = [[WIDTH + offset, laser_y], [WIDTH + offset, larg_laser, laser_y]]
        case 1:
            alt_laser = random.randint(100, 300)
            laser_y = random.randint(100, HEIGHT - 400)
            atualiza_laser = [[WIDTH + offset, laser_y], [WIDTH + offset, laser_y + alt_laser]]
    return atualiza_laser



game = True 

pygame.mixer.music.play(loops=-1)

while game:
    timer.tick(fps)
    if contador < 40:
        contador += 1
    else:
        contador = 0
    if atualiza_laser:
        laser = laser_gerado()
        atualiza_laser = False

    linhas, teto_plat, chao_plat, laser, linha_do_laser = tela(linhas, laser)
    avatar = desenha_avatar()
    colisao, reviver, vida = vercolisao()

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
        distancia += velocidade
        if boost:
            v_y -= gravidade
        else:
            v_y += gravidade
        if (colisao[0] and v_y > 0) or (colisao[1] and v_y < 0):
            v_y = 0
        boneco_y += v_y 

    if distancia < 50000:
        velocidade = 1 + (distancia // 500) / 10
    else:
        velocidade = 11

    if laser[0][0] < 0 and laser[1][0] < 0:
        atualiza_laser = True

    if reviver:
        distance = 0
        pause = False
        boneco_y = init_y
        v_y = 0
        reviver = 0
        atualiza_laser = True
    
    if vida == 0:
        pygame.QUIT = True
        pontuacao = 0
    else:
        pygame.QUIT = False

    if distancia > pontuacao:
        pontuacao = int(distancia)

    pygame.display.update()
pygame.quit()