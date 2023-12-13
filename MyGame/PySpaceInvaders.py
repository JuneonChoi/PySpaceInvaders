import math
import random

import pygame
from pygame import mixer

from tkinter import *
from tkinter import messagebox

# Intialize the pygame
pygame.init()

# create the screen
s_width = 1200
s_height = 800
screen = pygame.display.set_mode((s_width, s_height))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Bullet (img size = 64 * 64px)

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImgs = []

for i in range(6):
    bulletImgs.append(pygame.image.load('bullet/bullet'+ str(i+1) +'.png'))

bulletImg_index = 0
bulletImg = bulletImgs[bulletImg_index]
bulletSound = mixer.Sound("laser.wav")
bullet_InScreen = 3
bullet = [[-100, -100, "ready"] for i in range(bullet_InScreen)]  #x,y,state
bulletY_change = 20

# Define the colors we will use in RGB format
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

def game():

    # Game Loop
    running = True
    
    clock = pygame.time.Clock()

    # Game Over
    over_font = pygame.font.Font('freesansbold.ttf', 64)

    # Score
    score_font = pygame.font.Font('freesansbold.ttf', 32)
    scoreX = 10
    scoreY = 10
    score_value = 0

    #Level
    level_font = pygame.font.Font('freesansbold.ttf', 32)
    levelX = s_width / 2 - 5  #txt size == 10 * 10
    levelY = 10
    level_value = 1
    level_max = 3
    level_next = 3

    # Player (img size = 136 * 136 px)
    playerImgs = []

    for i in range(24):
        playerImgs.append(pygame.image.load('player/player'+ str(i+1) +'.png'))

    playerImg_index = 0
    playerImg = playerImgs[playerImg_index]
    
    playerX = s_width / 2 - 136 // 2
    playerY = s_height - 136
    playerX_change = 0
    player_speed = 8

    # Enemy (img size = 64 * 64 px)
    enemyImg = []

    for i in range(level_max):
        enemyImg.append(pygame.image.load('enemy'+ str( i ) + '.png'))

    explosionSound = mixer.Sound("explosion.wav")
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = 70
    enemyX_limit = s_width - 64
    enemy_num = 6
    enemy_speed = 8  #default == 8

    #Initial enemy assign
    for i in range(enemy_num):
        enemyX.append(random.randrange(0, enemyX_limit, 70))  #enemy_size w/ some space == 70
        enemyY.append(random.randrange(50, 190, 70))
        enemyX_change.append(enemy_speed)


    def show_score(x, y):
        score = score_font.render("Score : " + str(score_value), True, white)
        screen.blit(score, (x, y))


    def show_level(x, y):
        level = level_font.render("Level  : " + str(level_value), True, red)
        screen.blit(level, (x, y))

    def game_over_text():
        over_text = over_font.render("GAME OVER", True, white)
        screen.blit(over_text, (200, 250))


    def player(x, y):
        screen.blit(playerImg, (x, y))


    def enemy(x, y, level):
        screen.blit(enemyImg[level], (x, y))


    def fire_bullet(bullet_num):
        global bullet
        global bulletImg
        bullet[bullet_num][2] = "fire"
        screen.blit(bulletImg, (bullet[bullet_num][0] + 64 // 2, bullet[bullet_num][1] + bulletY_change))


    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
        if distance < 42:
            return True
        else:
            return False

    while running:

        # RGB = Red, Green, Blue
        screen.fill(black)
        
        # Background Image
        screen.blit(background, (0, 0))

        #control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                ans = False  #Don't create message box to ask player
                return ans
            if event.type == pygame.KEYDOWN:
                #Quit
                if event.key == pygame.K_ESCAPE:
                    running = False
                    ans = False  #Don't create message box to ask player
                    return ans
                #Shoot
                if event.key == pygame.K_SPACE:
                    for i in range(len(bullet)):
                        if bullet[i][2] == "ready":
                            bulletSound = mixer.Sound("laser.wav")
                            bulletSound.play()
                            # Get the current x cordinate of the spaceship
                            bullet[i][0] = playerX
                            fire_bullet(i)
                            
        #Player movement
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if playerX <= 0:
                playerX = 0
            else:
                playerX -= player_speed
        elif keys[pygame.K_RIGHT]:
            if playerX >= s_width - 64:
                playerX = s_width - 64
            else:
                playerX += player_speed

        # Level System
        if score_value == level_next:
            if level_value < level_max:
                level_value += 1
                level_next += level_next
                enemy_speed += enemy_speed // 4
                enemy_num += level_value
                
                for i in range(enemy_num):  #For not to be out of index
                    enemyX.append(random.randrange(0, enemyX_limit, 70))
                    enemyY.append(random.randrange(50, 190, 70))
                    enemyX_change.append(enemy_speed)

        
        for i in range(enemy_num):

            # Game Over
            if enemyY[i] > playerY :
                for j in range(enemy_num):
                    enemyY[j] = 9999  #Enemy disapear when game overs
                game_over_text()
                ans = messagebox.askretrycancel("askretrycancel", "Try again?")
                root=Tk()
                root.destroy()
                return ans
                break
            
            # Enemy Movement - 1
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = enemy_speed
                enemyY[i] += enemyY_change
            elif enemyX[i] >= enemyX_limit:
                enemyX_change[i] = -enemy_speed
                enemyY[i] += enemyY_change
                
            # Collision
            for j in range(len(bullet)):
                collision = isCollision(enemyX[i], enemyY[i], bullet[j][0], bullet[j][1])
                if collision:
                    explosionSound = mixer.Sound("explosion.wav")
                    explosionSound.play()
                    bullet[j][1] = playerY
                    bullet[j][2] = "ready"
                    score_value += 1
                    enemyX[i] = random.randrange(0, enemyX_limit, 70)  #enemy_size w/ some space == 70
                    enemyY[i] = random.randrange(50, 190, 70)
                    
            # Enemy Movement - 2
            enemy(enemyX[i], enemyY[i], level_value - 1)
            
        # Bullet Movement
        for j in range(len(bullet)):
            if bullet[j][1] <= - 64:
                bullet[j][1] = playerY
                bullet[j][2] = "ready"

            if bullet[j][2] == "fire":
                fire_bullet(j)
                bullet[j][1] -= bulletY_change

        player(playerX, playerY)
        show_score(scoreX, scoreY)
        show_level(levelX, levelY)
        pygame.display.update()

         # Animation sprite index cycle        
        playerImg_index += 1
        if playerImg_index >= len(playerImgs):
            playerImg_index = 0
        playerImg = playerImgs[playerImg_index]

        global bulletImg_index
        bulletImg_index += 1
        if bulletImg_index >= len(bulletImgs):
            bulletImg_index = 0
        bulletImg = bulletImgs[bulletImg_index]

        pygame.display.flip()
        clock.tick(60)

    #Ask if player wants to restart
    ans = messagebox.askretrycancel("askretrycancel", "Try again?")
    root=Tk()
    root.destroy()
    return ans

#If player choose yes in message box, restart the game
while True:
  if game() == True:
    pass
  else:
    break
