import pygame
import random

pygame.init()

# Window
screen = pygame.display.set_mode((800, 900))

#Background

background = pygame.image.load('Level1City.png')

#Title
pygame.display.set_caption("Mayday")
icon = pygame.image.load('SpaceShooterIcon.png')
pygame.display.set_icon(icon)

#Ship
playerimg = pygame.image.load('ShipBase.png')
playerX = 325
playerY = 700
playerMovementX = 0
playerMovementY = 0

#Enemies
enemy1img = pygame.image.load('Enemy1.png')
enemy1X = random.randint(0, 789)
enemy1Y = -200
enemy1X_change = 0.3
enemy1Y_change = 0.3

enemy2img = pygame.image.load('Enemy2.png')
enemy2X = random.randint(0, 789)
enemy2Y = -300
enemy2X_change = 8
enemy2Y_change = 0.3

# Projectiles

bullet1img = pygame.image.load('BulletShip.png')

bullets = []

bullet_speed = 10

#Auto
shoot_delay = 150
last_shot = 0
shooting = False


def player(x,y):
    screen.blit(playerimg, (x, y))

def enemy(x,y):
    screen.blit(enemy1img, (x, y))

def enemy2(x,y):
    screen.blit(enemy2img, (x, y))    

def draw_bullets():
    for bullet in bullets:
        screen.blit(bullet1img, (bullet[0], bullet[1]))

#Game Loop
running = True
while running:

    #Base Background
    
    #Background
    screen.blit(background, (0, 0))
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerMovementX = -5
            if event.key == pygame.K_RIGHT:
                playerMovementX = 5 
            if event.key == pygame.K_UP:
                 playerMovementY = -5
            if event.key == pygame.K_DOWN:
                playerMovementY = 5 
            if event.key == pygame.K_SPACE:
                shooting = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_SPACE:
                playerMovementX = 0 
                playerMovementY = 0
                shooting = False            
            
   


    playerX += playerMovementX
    playerY += playerMovementY

    #Boundary

    #PlayerBounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 672:
        playerX = 672  
    if playerY <=0:
        playerY = 0
    elif playerY >=   772:
        playerY = 772

    #Enemy Bounds

    #Enemy Basic
    enemy1Y += enemy1Y_change

    if enemy1Y >= -200:
        enemy1Y_change = 2     

    #Enemy Fast
    enemy2X += enemy2X_change
    enemy2Y += enemy2Y_change

    if enemy2X <= 0:
        enemy2X_change = 8
    elif enemy2X>= 672:
        enemy2X_change = -8
    if enemy2Y >= -300:
        enemy2Y_change = 0.5  

    #Bullet   

    #Auto-Fire
    current_time = pygame.time.get_ticks()

    if shooting:
        if current_time - last_shot > shoot_delay:
            bullets.append([playerX + 30, playerY +15])
            last_shot = current_time

    #Movemement
    for bullet in bullets:
        bullet[1] -= bullet_speed

    #Removing
    bullets = [bullet for bullet in bullets if bullet [1]> - 50]    

    player(playerX, playerY)
    enemy(enemy1X, enemy1Y)
    enemy2(enemy2X, enemy2Y)

    draw_bullets()

    pygame.display.update()
