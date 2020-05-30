import random
import winsound
import pygame
from pygame.locals import *
import sys

FPS = 30
WINDOWWIDTH = 600
WINDOWHEIGHT = 800

GRAY = (100, 100, 100)
NAVYBLUE = ( 60, 60, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = ( 0, 255, 255)
BGCOLOR = (0, 0, 0)

player_x = 300
player_y = 700

number_of_enemies = 15
enemies = []
enemy_speed = 2

class enemy(pygame.sprite.Sprite):
    image = pygame.image.load(r'invader.gif')

    def __init__(self, xcor, ycor):
        self.xcor = xcor
        self.ycor = ycor
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(self.xcor, self.ycor, 24, 24)

class player(pygame.sprite.Sprite):
    image = pygame.image.load(r'player.gif')

    def __init__(self, xcor, ycor):
        self.xcor = xcor
        self.ycor = ycor
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(self.xcor, self.ycor, 23, 15)

class bullet(pygame.sprite.Sprite):
    image = pygame.image.load(r'bullet.gif')
    state = "ready"

    def __init__(self, xcor, ycor):
        self.xcor = xcor
        self.ycor = ycor
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(self.xcor, self.ycor, 3, 11)

new_player = player(300, 700)

playerspeed = 15

score = 0

bulletspeed = 20
bulletstate = "ready"

game_over = False

new_bullet = bullet(new_player.xcor, new_player.ycor)

global FPSCLOCK, DISPLAYSURF

pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Space Invaders')
DISPLAYSURF.fill(BGCOLOR)

def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

def message_display(xcor, ycor, text):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (xcor, ycor)
    DISPLAYSURF.blit(TextSurf, TextRect)

def move_left():
    new_player.xcor -= playerspeed
    if new_player.xcor < 20:
        new_player.xcor = 20
    DISPLAYSURF.blit(new_player.image, (new_player.xcor, new_player.ycor))

def move_right():
    new_player.xcor += playerspeed
    if new_player.xcor > 560:
        new_player.xcor = 560
    DISPLAYSURF.blit(new_player.image, (new_player.xcor, new_player.ycor))

def fire_bullet():
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "fire"
        winsound.PlaySound("laser", winsound.SND_ASYNC)
        new_bullet.xcor = new_player.xcor + 10
        new_bullet.ycor = new_player.ycor - 10
        DISPLAYSURF.blit(new_bullet.image, (new_bullet.xcor, new_bullet.ycor))

#Check for an enemy collision at 2 coordinates
def enemy_collision(x, y):
    for e in enemies:
        if e.hitbox.colliderect(pygame.Rect(x, y, 24, 24)):
            return True
    return False

#Generate a spawn coordinate that doesn't collide with another enemy
def enemy_spawn_generator():
    while True:
        xcor = random.randint(50, 500)
        ycor = random.randint(50, 200)
        if not enemy_collision(xcor, ycor):
            break
    return (xcor, ycor)

#Initial enemy spawner
for i in range(number_of_enemies):
    enemies.append(enemy(*enemy_spawn_generator()))
    DISPLAYSURF.blit(enemies[i].image, (enemies[i].xcor, enemies[i].ycor))
    enemies[i].hitbox = pygame.Rect((enemies[i].xcor, enemies[i].ycor, 24, 24))

#Main game loop
while True:
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(new_player.image, (new_player.xcor, new_player.ycor))
    new_player.hitbox = (new_player.xcor, new_player.ycor, 23, 15)
    pygame.draw.rect(DISPLAYSURF, WHITE, (20, 20, 560, 760), 4)

    message_display(70, 40, "SCORE: ")
    message_display(120, 40, str(score))

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                move_left()
            elif event.key == K_RIGHT:
                move_right()
            elif event.key == K_SPACE:
                fire_bullet()

    for e in enemies:
        e.xcor += enemy_speed
        DISPLAYSURF.blit(e.image, (e.xcor, e.ycor))
        e.hitbox = pygame.Rect((e.xcor, e.ycor, 24, 24))

        if e.xcor > 560:
            for e in enemies:
                e.ycor += 20
                DISPLAYSURF.blit(e.image, (e.xcor, e.ycor))
            enemy_speed *= -1

        if e.xcor < 20:
            for e in enemies:
                e.ycor += 20
                DISPLAYSURF.blit(e.image, (e.xcor, e.ycor))
            enemy_speed *= -1

        if e.hitbox.colliderect(new_player.hitbox):
            winsound.PlaySound("explosion", winsound.SND_ASYNC)
            new_player.ycor = 1000
            game_over = True


    if bulletstate == "fire":
        new_bullet.ycor -= bulletspeed
        DISPLAYSURF.blit(new_bullet.image, (new_bullet.xcor, new_bullet.ycor))
        new_bullet.hitbox = (new_bullet.xcor, new_bullet.ycor, 3, 11)

        for e in enemies:
            if e.hitbox.colliderect(new_bullet.hitbox):
                winsound.PlaySound("explosion", winsound.SND_ASYNC)
                enemies.remove(e)
                score += 10
                new_bullet.xcor = -20
                new_bullet.ycor = -20
                bulletstate = "ready"

    if new_bullet.ycor < 40:
        new_bullet.xcor = -20
        new_bullet.ycor = -20
        bulletstate = "ready"

    if game_over == True:
        message_display(300, 400, "GAME OVER")
        enemies.clear()

    if not enemies:
        message_display(300, 400, "YOU WIN!")
    pygame.display.update()
    FPSCLOCK.tick(FPS)
