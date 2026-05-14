import pygame
import random
import math
import sys
import os

pygame.init()
pygame.mixer.init()

def reset_game():
    global playerX, playerY, player_health
    global enemy1X, enemy1Y, enemy1_health
    global enemy2X, enemy2Y, enemy2_health
    global bullets, enemy1_bullets, enemy2_bullets
    global score

    playerX = 325
    playerY = 700
    player_health = 3

    enemy1X = random.randint(0, 789)
    enemy1Y = -50
    enemy1_health = 8

    enemy2X = random.randint(0, 789)
    enemy2Y = -100
    enemy2_health = 4

    bullets = []
    enemy1_bullets = []
    enemy2_bullets = []

    score = 0

game_over = False
menu = True

# Window
screen = pygame.display.set_mode((800, 900))

#Background

gameoverscreen = pygame.image.load('ScreenGameOver.png')
menuscreen = pygame.image.load('ScreenMenu.png')
background = pygame.image.load('Level1City.png')
bg_y = 0
bg_speed = 2
bg_height = background.get_height()

score = 0
font = pygame.font.SysFont("impact", 30)

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
invicibility_time = 2000

#Enemies
enemy1img = pygame.image.load('Enemy1.png')
enemy1X = random.randint(0, 789)
enemy1Y = -50
enemy1Y_change = 1.2
enemy1_health = 8

enemy2img = pygame.image.load('Enemy2.png')
enemy2X = random.randint(0, 789)
enemy2Y = -100
enemy2X_change = 8
enemy2Y_change = 1.5
enemy2_health = 4

# Projectiles

#Player Bullets
bullet1img = pygame.image.load('BulletShip.png')
bullets = []
bullet_speed = 10

#AutoFire
shoot_delay = 75
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

#Sound effects

menu_music = "EschatosNameEntry.mp3"
game_music = "EschatosStage2.mp3"
gameover_music = "EschatosGameOver.mp3"

#SFX
player_channel = pygame.mixer.Channel(0)
player_shoot_sound = pygame.mixer.Sound("ShipFire.wav")
player_ship_hit = pygame.mixer.Sound("ShipHit.wav")
player_ship_hit_final = pygame.mixer.Sound("ShipWarning.wav")
enemy_shoot_sound = pygame.mixer.Sound("FireMed.wav")
enemy2_shoot_sound = pygame.mixer.Sound("FireSmall.wav")
enemy_destroyed_sound = pygame.mixer.Sound("Explosion.wav")


#SFX Volume
player_shoot_sound.set_volume(0.5)
enemy_shoot_sound.set_volume(0.9)
enemy2_shoot_sound.set_volume(0.1)
enemy_destroyed_sound.set_volume(0.7)
player_ship_hit.set_volume(0.6)
player_ship_hit_final.set_volume(0.5)

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

#Menu Music
pygame.mixer.music.load(menu_music)
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

while menu:

    screen.blit(menuscreen, (0, 0))
    small_font = pygame.font.SysFont("impact", 32)
    start_text = small_font.render("Press ENTER to Start", True, (255, 255, 255))
    quit_text = small_font.render("Press ESC to Quit", True, (255, 255, 255))

    screen.blit(start_text, (250, 400))
    screen.blit(quit_text, (270, 450))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RETURN:
                menu = False

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

#Game Loop
running = True

#Game Music
pygame.mixer.music.stop()
pygame.mixer.music.load(game_music)
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

while running:
   
    #Background
    bg_y += bg_speed

    bg_y = (bg_y +  bg_speed) % bg_height

    screen.blit(background, (0, bg_y))
    screen.blit(background, (0, bg_y - bg_height))       
        
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
                if player_channel.get_busy():
                    player_channel.stop()  

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

    if enemy1Y > 900:
        enemy1X = random.randint(0, 700)
        enemy1Y = -100
        score -= 20  

    #Enemy Fast
    enemy2X += enemy2X_change
    enemy2Y += enemy2Y_change

    if enemy2X <= 0:
        enemy2X_change = 8
    elif enemy2X>= 672:
        enemy2X_change = -8
    if enemy2Y >= -300:
        enemy2Y_change = 0.5  

    if enemy2Y > 900:
        enemy2X = random.randint(0, 700)
        enemy2Y = -150
        enemy2_health = 4
        score -= 30    

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

            player_shoot_sound.play()

    #Enemy Projectiles
    
    #Enemy 1 Bullets

    if current_time - enemy1_last_shot > enemy1_shoot_delay:

        enemy_shoot_sound.play()

        enemy1_bullets.append([
            enemy1X + enemy1img.get_width() // 2,
            enemy1Y + bullet2img.get_height()
        ])

        enemy1_last_shot = current_time
    
    #Enemy 2 Bullets

    if current_time - enemy2_last_shot > enemy2_shoot_delay:

        enemy2_shoot_sound.play()

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
                enemy1_health = 60

                score += 10

                enemy_destroyed_sound.play()    

        #Enemy 2 Health & Damage
        elif bullet_rect.colliderect(enemy2_rect):
            bullets.remove(bullet)
            enemy2_health -= 1

            if enemy2_health <= 0:    
                enemy2X = random.randint(0,700)
                enemy2Y = -300
                enemy2_health = 100

                score += 15

                enemy_destroyed_sound.play()    

    #Player DMG & HP

    now = pygame.time.get_ticks()

    for bullet in enemy1_bullets[:]:

        bullet_rect =  pygame.Rect(
            bullet[0],
            bullet[1],
            10,
            20
        )

        if bullet_rect.colliderect(player_rect):
            enemy1_bullets.remove(bullet)

            if now - player_hit_time >= invicibility_time:

                player_health -= 1
                player_hit_time = now

            if player_health == 1:
                player_ship_hit_final.play()
            else:
                player_ship_hit.play()        

    for bullet in enemy2_bullets[:]:

        bullet_rect =  pygame.Rect(
            bullet[0],
            bullet[1],
            10,
            20
        )

        if bullet_rect.colliderect(player_rect):
            enemy2_bullets.remove(bullet)

            if now - player_hit_time >= invicibility_time:

                player_health -= 1
                player_hit_time = now

            if player_health == 1:
                player_ship_hit_final.play()
            else:
                player_ship_hit.play()                             
            
    #Removing
    bullets = [bullet for bullet in bullets if bullet [1]> - 50]  

    enemy1_bullets = [bullet for bullet in enemy1_bullets if bullet [1] < 950]

    enemy2_bullets = [bullet for bullet in enemy2_bullets if bullet [1]< 950] 

    #Game Over
    if player_health <= 0:
        game_over = True
        running = False 

    #Drawing
    now = pygame.time.get_ticks()
    invincible = now - player_hit_time < invicibility_time
    
    #Blinking Effect when Damaged
    if invincible:
        if (now // 100) % 2 == 0: 
            temp_img = playerimg.copy()
            temp_img.set_alpha(120)  
            screen.blit(temp_img, (playerX, playerY))
    else:
        player(playerX, playerY)
    enemy(enemy1X, enemy1Y)
    enemy2(enemy2X, enemy2Y)

    draw_bullets()
    draw_enemy2_bullets()
    draw_enemy3_bullets()

    score_text = font.render(f"score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()

#Game Over Music
pygame.mixer.music.stop()  
pygame.mixer.music.load(gameover_music)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play (1)

while game_over:

    screen.blit(gameoverscreen, (0, 0))
    small_font = pygame.font.SysFont("arial", 32)

    score_text = small_font.render(f"Final Score: {score}", True, (255, 255, 255))
    restart_text = small_font.render("Press R to Restart or ESC to Quit", True, (255, 255, 255))

    screen.blit(score_text, (300, 380))
    screen.blit(restart_text, (200, 450))

    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN: 

            if event.key == pygame.K_r:
                reset_game()
                game_over = False
                running = True
                break

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()         
