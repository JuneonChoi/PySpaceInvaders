import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# Define the colors we will use in RGB format
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

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

# Player
playerImg = pygame.image.load('player.png')
playerX = s_width / 2 - 32
playerY = s_height - 120
playerX_change = 0

# Enemy
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
enemy_speed = 3  #default == 3

for i in range(enemy_num):
    enemyX.append(random.randrange(0, enemyX_limit, 70))  #enemy_size w/ some space == 70
    enemyY.append(random.randrange(50, 190, 70))
    enemyX_change.append(enemy_speed)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletSound = mixer.Sound("laser.wav")
bullet_InScreen = 3
bullet = [[0, 0, "ready"] for i in range(bullet_InScreen)]  #x,y,state
bulletY_change = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


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
    bullet[bullet_num][2] = "fire"
    screen.blit(bulletImg, (bullet[bullet_num][0] + 16, bullet[bullet_num][1] + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                for i in range(len(bullet)):
                    if bullet[i][2] == "ready":
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        # Get the current x cordinate of the spaceship
                        bullet[i][0] = playerX
                        fire_bullet(i)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= enemyX_limit:
        playerX = enemyX_limit

    # Level System
    if score_value == level_next:
        if level_value < level_max:
            level_value += 1
            level_next += level_next

            enemy_speed += level_value - 1
            enemy_num += level_value
            
            for i in range(enemy_num):  #for not to be out of index
                enemyX.append(random.randrange(0, enemyX_limit, 70))
                enemyY.append(random.randrange(50, 190, 70))
                enemyX_change.append(enemy_speed)

    # Enemy Movement
    for i in range(enemy_num):

        # Game Over
        if enemyY[i] > playerY - 40:
            for j in range(enemy_num):
                enemyY[j] = 9999
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change
        elif enemyX[i] >= enemyX_limit:
            enemyX_change[i] = -enemy_speed
            enemyY[i] += enemyY_change
        for j in range(len(bullet)):
            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bullet[j][0], bullet[j][1])
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bullet[j][1] = playerY
                bullet[j][2] = "ready"
                score_value += 1
                enemyX[i] = random.randrange(0, enemyX_limit, 70)  #enemy_size w/ some space == 70
                enemyY[i] = random.randrange(50, 190, 70)

        enemy(enemyX[i], enemyY[i], level_value - 1)
        
    # Bullet Movement
    for j in range(len(bullet)):
        if bullet[j][1] <= 0:
            bullet[j][1] = playerY
            bullet[j][2] = "ready"

        if bullet[j][2] == "fire":
            fire_bullet(j)
            bullet[j][1] -= bulletY_change

    player(playerX, playerY)
    show_score(scoreX, scoreY)
    show_level(levelX, levelY)
    pygame.display.update()
