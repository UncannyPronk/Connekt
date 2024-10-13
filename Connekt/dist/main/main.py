import pygame, socket, sys
from pygame import *
from pygame.locals import *

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

def write(text='sample_text', pos=(0, 0), font="Arial", color=(255, 255, 255), size=20, bgcolor=None):
    textfont = pygame.font.SysFont(font, size)
    txt = textfont.render(text, True, color, bgcolor)
    screen.blit(txt, pos)

def text_input(prompt="Enter text:"):
    text = ""
    running = True
    key_time = 0
    while running:
        pygame.display.flip(); clock.tick(30)
        pygame.draw.rect(screen, (0, 0, 0), (0, 280, 800, 80))
        write(str(prompt), (50, 300), size=38, color=(160, 0, 0))
        write(str(text), (400, 300), size=38, color=(180, 255, 200))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_DELETE:
                    text = ""
                if event.key == K_BACKSPACE:
                    text = text[:-1]
                elif event.key == K_RETURN:
                    return text
                elif event.key == K_MINUS:
                    text += "_"
                elif event.key == K_SPACE:
                    text += " "
                elif len(text) < 16:
                    text += event.unicode
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_BACKSPACE] and len(text) > 0:
            key_time += 0.1
            if key_time > 3:
                text = text[:-1]
        else:
            key_time = 0
    return text

ip = text_input("Enter server address: ")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, 5000))

name = text_input("Enter your name: ")
s.send(name.encode())

tilemap = []
with open("map.txt", "r") as mapfile:
    for line in mapfile.readlines():
        tilemap.append([])
        for i in line:
            if i != "\n":
                tilemap[-1].append(int(i))

class Box():
    def __init__(self):
        self.x = 100
        self.y = 160
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
        box.y -= 4
    elif keys_pressed[K_s] and box.rect.bottom < SCREEN_HEIGHT:
        box.y += 4
    if keys_pressed[K_a] and box.rect.x > 0:
        box.x -= 4
    elif keys_pressed[K_d] and box.rect.right < SCREEN_WIDTH:
        box.x += 4
    box.rect.x = box.x - 10
    box.rect.y = box.y - 10
    screen.fill((0, 0, 0))
    rects = []
    for y in range(len(tilemap)):
        for x in range(len(tilemap[y])):
            if tilemap[y][x] == 1:
                pygame.draw.rect(screen, (20, 200, 220), (20+(x*50), y*50, 50, 50))
                rects.append(Rect(20+(x*40), y*40, 40, 40))
            elif tilemap[y][x] == 2:
                pygame.draw.rect(screen, (225, 0, 0), ((x*50)+25, (y*50)+5, 40, 40))

    for client in players_values_dict:
        if client != name:
            # pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(int(players_values_dict[client][0]), int(players_values_dict[client][1]), 20, 20))
            try:
                pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(int(players_values_dict[client][0]), int(players_values_dict[client][1]), 20, 20))
                write(str(client), (int(players_values_dict[client][0]) + 25, int(players_values_dict[client][1]) - 5))
            except ValueError:
                pass
    pygame.draw.rect(screen, box.color, box.rect)
    clock.tick(30)
    pygame.display.update()
    