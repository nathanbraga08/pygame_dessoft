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
velocidade = 5
pause = False
init_y = HEIGHT - 130
boneco_y = init_y
boost = False
contador = 0
v_y = 0 
gravidade = 0.4
atualiza_laser = True
laser = []
distancia = 0
reviver = False
mudacor = 0
missel_c = 0
missel_a = False
missel_delay = 0
missel_cord = []

# Carrega os sons do jogo
pygame.mixer.music.load('efeito-sonoro-hd.ogg')
pygame.mixer.music.set_volume(0.4)

file = open('teste.txt', 'r')
read = file.readlines()
maiorponto = int(read[0])
tvivo = int(read[1])
file.close()

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
    linha_do_laser = pygame.draw.line(window, 'red', (listalaser[0][0], listalaser[0][1]),(listalaser[1][0],listalaser[1][1]), 10)
    window.blit(font.render(f'distancia percorrida: {int(distancia)} m', True, 'white'), (10,10))
    window.blit(font.render(f'recorde: {int(maiorponto)} m', True, 'white'), (10,70))
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
    coll = [False, False]
    restart = False
    if avatar.colliderect(chao_plat):
        coll[0] = True
    elif avatar.colliderect(teto_plat):
        coll[1] = True
    if linha_do_laser.colliderect(avatar):
        restart = True
    if missel_a:
        if missel.colliderect(avatar):
            restart = True
    return coll, restart


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

def desenha_foguete(cordenada, modo):
    if modo == 0:
        pedra = pygame.draw.rect(window, 'dark red', [cordenada[0] - 60, cordenada[1] - 25, 50, 50], 0, 5)
        window.blit(font.render('!', True, 'black'), (cordenada[0] - 40, cordenada[1] - 20))
        if not pause:
            if cordenada[1] > boneco_y + 10:
                cordenada[1] -= 3
            else:
                cordenada[1] += 3
    else:
        pedra = pygame.draw.rect(window, 'red', [cordenada[0], cordenada[1] - 10, 50, 20], 0, 5)
        pygame.draw.ellipse(window, 'orange', [cordenada[0] + 50, cordenada[1] - 10, 50, 20], 7)
        if not pause:
            cordenada[0] -= 10 + velocidade

    return cordenada, pedra


def draw_pause():
    pygame.draw.rect(window, (128, 128, 128, 150), [0, 0, WIDTH, HEIGHT])
    restart_btn = pygame.draw.rect(window, 'white', [200, 220, 280, 50], 0, 10)
    window.blit(font.render('Continuar', True, 'black'), (220, 230))
    quit_btn = pygame.draw.rect(window, 'white', [520, 220, 280, 50], 0, 10)
    window.blit(font.render('Sair', True, 'black'), (540, 230))
    return restart_btn, quit_btn

def modify_player_info():
    global maiorponto, tvivo
    if distancia > maiorponto:
        maiorponto = distancia
    tvivo += distancia
    file = open('teste.txt', 'w')
    file.write(str(int(maiorponto)) + '\n')
    file.write(str(int(tvivo)))
    file.close()


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
    if pause:
        restart, quits = draw_pause()

    if not missel_a and not pause:
        missel_c += 1
    if missel_c > 180:
        missel_c = 0
        missel_a = True
        missel_delay = 0
        missel_cord = [WIDTH, HEIGHT/2]
    if missel_a:
        if missel_delay < 90:
            if not pause:
                missel_delay += 1
            missel_cord, missel = desenha_foguete(missel_cord, 0)
        else:
            missel_cord, missel = desenha_foguete(missel_cord, 1)
        if missel_cord[0] < -50:
            missel_a = False

    avatar = desenha_avatar()
    colisao, reviver = vercolisao()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            modify_player_info()
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if pause:
                    pause = False
                else:
                    pause = True
            if event.key == pygame.K_SPACE and not pause:
                boost = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                boost = False
        if event.type == pygame.MOUSEBUTTONDOWN and pause:
            if restart.collidepoint(event.pos):
                reviver = True
            if quits.collidepoint(event.pos):
                modify_player_info()
                run = False

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

    if distancia - mudacor > 500:
        mudacor = distancia
        fundo = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    if reviver:
        modify_player_info()
        distancia = 0
        missel_a = False
        missel_c  = 0
        pause = False
        boneco_y = init_y
        v_y = 0
        reviver = 0
        atualiza_laser = True

    if distancia > maiorponto:
        maiorponto = int(distancia)

    pygame.display.update()
pygame.quit()