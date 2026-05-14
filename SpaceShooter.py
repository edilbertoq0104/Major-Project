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
ShipMax = pygame.image.load('ShipBase.png')
ShipMid = pygame.image.load('ShipInjured1.png')
ShipLow = pygame.image.load('ShipInjured2.png')

playerimg = ShipMax

playerX = 325
playerY = 700

#Player HP
player_health = 3

#I-Frames
player_hit_time = 0
invicibility_time = 1000

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

#Player Bullets
bullet1img = pygame.image.load('BulletShip.png')
bullets = []
bullet_speed = 10

#AutoFire
shoot_delay = 150
last_shot = 0
shooting = False

#Enemy Bullets

#Enemy 1 Bullets
bullet2img = pygame.image.load('BulletEnemy1.png')
enemy1_bullets = []
enemy1_bullet_speed = 3

enemy1_shoot_delay = 700
enemy1_last_shot = 0

#Enemy 2 Bullets
bullet3img = pygame.image.load('BulletEnemy2.png')
enemy2_bullets = []
enemy2_bullet_speed = 2

enemy2_shoot_delay = 700
enemy2_last_shot = 0

def player(x,y):
    screen.blit(playerimg, (x, y))

def enemy(x,y):
    screen.blit(enemy1img, (x, y))

def enemy2(x,y):
    screen.blit(enemy2img, (x, y))    

def draw_bullets():
    for bullet in bullets:
        screen.blit(bullet1img, (bullet[0], bullet[1]))
#Enemy Bullet Type 1
def draw_enemy2_bullets():
    for bullet in enemy1_bullets:
        screen.blit(bullet2img, (bullet[0], bullet[1]))
#Enemy Bullet Type 2
def draw_enemy3_bullets():
    for bullet in enemy2_bullets:
        screen.blit(bullet3img, (bullet[0], bullet[1]))

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
      
        #Player Firing

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shooting = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                shooting = False  

    #Player DMG States

    if player_health == 3:
        playerimg = ShipMax

    elif player_health == 2:
        playerimg = ShipMid

    elif player_health == 1:
        playerimg = ShipLow                    

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

    #Projectiles   

    #PlayerBullets
    current_time = pygame.time.get_ticks()

    if shooting:
        if current_time - last_shot > shoot_delay:
            bullets.append([playerX + 15, playerY +25])
            bullets.append([playerX + 30, playerY +15])
            bullets.append([playerX + 90, playerY +15])
            bullets.append([playerX + 105, playerY +25])
            last_shot = current_time

    #Enemy Projectiles
    
    #Enemy 1 Bullets

    if current_time - enemy1_last_shot > enemy1_shoot_delay:

        enemy1_bullets.append([
            enemy1X + enemy1img.get_width() // 2,
            enemy1Y + bullet2img.get_height()
        ])

        enemy1_last_shot = current_time
    
    #Enemy 2 Bullets

    if current_time - enemy2_last_shot > enemy2_shoot_delay:

        enemy2_bullets.append([
            enemy2X + enemy2img.get_width() // 2,
            enemy2Y + bullet3img.get_height()
        ])

        enemy2_last_shot = current_time        

    #Projectile  Movement
     
    #Player Bullet Movements         
    for bullet in bullets:
        bullet[1] -= bullet_speed

    #Enemy 1 Bullet Movements

    for bullet in enemy1_bullets:
        bullet[1] += enemy1_bullet_speed

    #Enemy 2 Bullet Movements

    for bullet in enemy2_bullets:
        bullet[1] += enemy2_bullet_speed

    #Collision

    #Enemy Collission

    enemy1_rect = pygame.Rect(enemy1X, enemy1Y,
                              enemy1img.get_width(),
                              enemy1img.get_height()) 
    
    enemy2_rect = pygame.Rect(enemy2X, enemy2Y,
                              enemy2img.get_width(),
                              enemy2img.get_height()) 

    #Player Collission

    player_rect = pygame.Rect(playerX + 40, playerY + 40,
                              playerimg.get_width() - 80,
                              playerimg.get_height()- 120) 
    
    #HP & DMG

    for bullet in bullets [:]:
        bullet_rect = get_bullet_rect(bullet)

        #Enemy 1 Health & Damage
        if bullet_rect.colliderect(enemy1_rect):
            bullets.remove(bullet)
            enemy1_health -= 1

            if enemy1_health <= 0:    
                enemy1X = random.randint(0,700)
                enemy1Y = -200
                enemy1_health = 8

        #Enemy 2 Health & Damage
        elif bullet_rect.colliderect(enemy2_rect):
            bullets.remove(bullet)
            enemy2_health -= 1

            if enemy2_health <= 0:    
                enemy2X = random.randint(0,700)
                enemy2Y = -300
                enemy2_health = 4

    #Player DMG & HP

    for bullet in enemy1_bullets[:]:

        bullet_rect =  pygame.Rect(
            bullet[0],
            bullet[1],
            10,
            20
        )

        if bullet_rect.colliderect(player_rect):
            enemy1_bullets.remove(bullet)

            if pygame.time.get_ticks() - player_hit_time > invicibility_time:

                player_health -= 1
                player_hit_time = pygame.time.get_ticks()

    for bullet in enemy2_bullets[:]:

        bullet_rect =  pygame.Rect(
            bullet[0],
            bullet[1],
            10,
            20
        )

        if bullet_rect.colliderect(player_rect):
            enemy2_bullets.remove(bullet)

            if pygame.time.get_ticks() - player_hit_time > invicibility_time:

                player_health -= 1
                player_hit_time = pygame.time.get_ticks()            
            
    #Removing
    bullets = [bullet for bullet in bullets if bullet [1]> - 50]  

    enemy1_bullets = [bullet for bullet in enemy1_bullets if bullet [1] < 950]

    enemy2_bullets = [bullet for bullet in enemy2_bullets if bullet [1]< 950] 

    #Game Over
    if player_health <= 0:
        running = False 

    #Drawing
    player(playerX, playerY)
    enemy(enemy1X, enemy1Y)
    enemy2(enemy2X, enemy2Y)

    draw_bullets()

    draw_enemy2_bullets()
    draw_enemy3_bullets()

    pygame.display.update()
