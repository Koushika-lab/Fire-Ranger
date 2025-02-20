import math
import random

import pygame
#from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('resources/background.png')

# Sound
pygame.mixer.music.load("resources/Starseed-chosic.com_.mp3")
pygame.mixer.music.play(loops=-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('resources/spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('resources/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Arrange enemies in a line
enemy_row_count = 1  # Number of rows of enemies
enemy_column_count = num_of_enemies  # Number of columns of enemies
enemy_spacing = 100  # Space between enemies
enemy_start_x = 50  # Starting X position for the line of enemies
enemy_start_y = 50  # Starting Y position for the line of enemies

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('resources/enemy.png'))
    enemyX.append(enemy_start_x + i * enemy_spacing)
    enemyY.append(enemy_start_y)
    enemyX_change.append(2)
    enemyY_change.append(30)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('resources/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

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

move_direction = 1  # 1 for right, -1 for left
move_change_interval = 30  # Number of frames to change direction

# Game Loop
running = True

frame_count = 0  # Track the number of frames

while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    frame_count += 1  # Increment frame count


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
                if bullet_state is "ready":
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
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        if frame_count % move_change_interval == 0:
            enemyX_change[i] *= move_direction

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_change[i] *= -1  # Change direction
            enemyY[i] += enemyY_change[i]  # Move down

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            #explosionSound = mixer.Sound("explosion.wav")
            #explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
    
