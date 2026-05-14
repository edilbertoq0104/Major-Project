import pygame
import random
import math

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

#Enemies
enemy1img = pygame.image.load('Enemy1.png')
enemy1X = random.randint(0, 789)
enemy1Y = -200
enemy1Y_change = 0.3
enemy1_health = 8

enemy2img = pygame.image.load('Enemy2.png')
enemy2X = random.randint(0, 789)
enemy2Y = -300
enemy2X_change = 8
enemy2Y_change = 0.3
enemy2_health = 4

# Projectiles
bullet1img = pygame.image.load('BulletShip.png')
bullets = []
bullet_speed = 10

#AutoFire
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

def get_bullet_rect(bullet):
    return pygame.Rect(bullet[0], bullet [1], 10, 20)

#Game Loop
running = True
while running:
   
    #Background
    screen.blit(background, (0, 0))
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shooting = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                shooting = False    

    # Movement

    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if keys[pygame.K_LEFT]:
        dx -= 1
    if keys[pygame.K_RIGHT]:
        dx += 1
    if keys[pygame.K_UP]:
        dy -= 1
    if keys[pygame.K_DOWN]:
        dy += 1 

    length = math.hypot(dx, dy)
    if length != 0:
        dx /= length
        dy /= length

    speed = 10

    playerX += dx * speed
    playerY += dy * speed      

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
            bullets.append([playerX + 15, playerY +25])
            bullets.append([playerX + 30, playerY +15])
            bullets.append([playerX + 90, playerY +15])
            bullets.append([playerX + 105, playerY +25])
            last_shot = current_time

    #Movemement
    for bullet in bullets:
        bullet[1] -= bullet_speed

    #Collision

    enemy1_rect = pygame.Rect(enemy1X, enemy1Y,
                              enemy1img.get_width(),
                              enemy1img.get_height()) 
    
    enemy2_rect = pygame.Rect(enemy2X, enemy2Y,
                              enemy2img.get_width(),
                              enemy2img.get_height()) 

    for bullet in bullets [:]:
        bullet_rect = get_bullet_rect(bullet)

        if bullet_rect.colliderect(enemy1_rect):
            bullets.remove(bullet)
            enemy1_health -= 1

            if enemy1_health <= 0:    
                enemy1X = random.randint(0,700)
                enemy1Y = -200
                enemy1_health = 8

        elif bullet_rect.colliderect(enemy2_rect):
            bullets.remove(bullet)
            enemy2_health -= 1

            if enemy2_health <= 0:    
                enemy2X = random.randint(0,700)
                enemy2Y = -300
                enemy2_health = 4

    #Removing
    bullets = [bullet for bullet in bullets if bullet [1]> - 50]  

    player(playerX, playerY)
    enemy(enemy1X, enemy1Y)
    enemy2(enemy2X, enemy2Y)
    draw_bullets()

    pygame.display.update()
