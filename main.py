import pygame, socket, sys, json
from pygame import *
from pygame.locals import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 5000))

name = input("Enter your name: ")
s.send(name.encode())

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Box():
    def __init__(self):
        self.x = 10
        self.y = 10
        self.rect = pygame.Rect(0, 0, 20, 20)
        self.color = (255, 255, 255)

box = Box()

running = True
while running:
    s.send((f"{box.rect.x}, {box.rect.y}*").encode())
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            s.close()
            pygame.quit()
            sys.exit()

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[K_w] and box.rect.y > 0:
        box.y -= 1
    elif keys_pressed[K_s] and box.rect.bottom < SCREEN_HEIGHT:
        box.y += 1
    if keys_pressed[K_a] and box.rect.x > 0:
        box.x -= 1
    elif keys_pressed[K_d] and box.rect.right < SCREEN_WIDTH:
        box.x += 1
    box.rect.x = box.x - 10
    box.rect.y = box.y - 10
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, box.color, box.rect)
    pygame.display.update()
    