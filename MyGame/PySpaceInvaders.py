import math
import random

import pygame
from pygame import mixer

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

# Player
playerImg = pygame.image.load('player.png')
playerX = s_width / 2 - 32
playerY = s_height - 120
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = 70
num_of_enemies = 9

enemyX_limit = s_width - 64

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randrange(0, enemyX_limit, 70))  #enemy_size w/ some space == 70
    enemyY.append(random.randrange(50, 190, 70))
    enemyX_change.append(4)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


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
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

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

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > playerY - 40:
            for j in range(num_of_enemies):
                enemyY[j] = 9999
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change
        elif enemyX[i] >= enemyX_limit:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randrange(0, enemyX_limit, 70)  #enemy_size w/ some space == 70
            enemyY[i] = random.randrange(50, 190, 70)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
