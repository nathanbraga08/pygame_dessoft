import pygame
import random

pygame.init()

WIDTH = 900
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jetpack')
fps = 60
timer = pygame.time.Clock()

game = True 
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False