import pygame

pygame.init()

# Window
screen = pygame.display.set_mode((800, 900))

#Title
pygame.display.set_caption("Mayday")
icon = pygame.image.load('SpaceShooterIcon.png')
pygame.display.set_icon(icon)

#Ship
playerimg = pygame.image.load('ShipBase.png')
playerX = 325
playerY = 700



def player(x,y):
    screen.blit(playerimg, (x, y))

#Game Loop
running = True
while running:

    #Base Background
    screen.fill((49, 0, 71))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False\
            
    screen.fill((49, 0, 71))

    player(playerX, playerY)
    pygame.display.update()
