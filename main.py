import pygame, socket, sys, json
from pygame import *
from pygame.locals import *

ip = input("Enter server address: ")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, 5000))

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
players_values_dict = {}

running = True
while running:
    s.send((f"{box.rect.x}, {box.rect.y}*").encode())
    players_values = s.recv(1024).decode()
    # players_values = "{'*jana': '0, 0-!', '*bro': '0, 0-!', '*man': '0, 0-!'}"
    players_values = players_values[1:-1]
    players_values = players_values.split('*')
    players_values = players_values[1:]
    newstring = ""
    for i in players_values:
        for j in i:
            if j != "'":
                newstring += j
    players_values = newstring
    players_values = players_values.split("!")
    print(players_values)
    for i in range(len(players_values)):
        if i != 0:
            players_values[i] = players_values[i][2:]
    players_values.pop()
    newstring = ""
    for i in range(len(players_values)):
        for j in players_values[i]:
            if j != ",":
                newstring += j
    players_values = newstring[:-1]
    players_values = players_values.split("-")
    for i in range(len(players_values)):
        players_values[i] = players_values[i].split(": ")
        players_values[i][1] = players_values[i][1].split(" ")
    # print(players_values)
    players_values_dict = {}
    for i in range(len(players_values)):
        players_values_dict[players_values[i][0]] = players_values[i][1]
    # print(players_values_dict)

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
    for client in players_values_dict:
        if client != name:
            # pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(int(players_values_dict[client][0]), int(players_values_dict[client][1]), 20, 20))
            try:
                pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(int(players_values_dict[client][0]), int(players_values_dict[client][1]), 20, 20))
            except ValueError:
                screen.fill((0, 0, 0))
    pygame.draw.rect(screen, box.color, box.rect)
    pygame.display.update()
    