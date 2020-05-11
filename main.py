import pygame
import random
import math
# Initialize pygame
pygame.init()

#create screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('Background.jpg')

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerImg = pygame.transform.scale(playerImg,(50,50))
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,750))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.85)
    enemyY_change.append(50)

# Torpedo

# Ready - You can't see the torpedo
# Fire - The torpedo is seen and moving
torpedoImg = pygame.image.load('torpedo.png')
torpedoImg = pygame.transform.scale(torpedoImg,(20,20))
torpedoX = 0
torpedoY = 470
torpedoX_change = 0
torpedoY_change = 1.5
torpedo_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf',128)

def show_score(x,y):
    score = font.render("SCORE = " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))
def game_over_text():
    over_text = font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (300,250))
def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y, i):
    screen.blit(enemyImg[i], (x,y))

def fire_torpedo(x,y):
    global torpedo_state
    torpedo_state = "fire"
    screen.blit(torpedoImg,(x + 16, y))


def isCollision(enemyX, enemyY, torpedoX, torpedoY):
    distance = math.sqrt((math.pow(enemyX-torpedoX,2)) + (math.pow(enemyY-torpedoY,2)))
    if distance < 28:
        return True
    else:
        return False
# Game loop
running = True
while running:

    # RGB values
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Checks if keystrokes are left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.1
            if event.key == pygame.K_SPACE:
                if torpedo_state == "ready":
                    #Get x coord of spaceship
                    torpedoX = playerX
                    fire_torpedo(torpedoX, torpedoY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

# Movement checking
    playerX += playerX_change

    if playerX > 750:
        playerX = 750
    elif playerX < 0:
        playerX = 0

    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] >430:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] > 750:
            enemyX_change[i] = -0.85
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] < 0:
            enemyX_change[i] = 0.85
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], torpedoX, torpedoY)
        if collision:
            torpedoY = 470
            torpedo_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 750)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # Torpedo Movement
    if torpedoY <=0:
        torpedoY = 470
        torpedo_state = "ready"
    if torpedo_state == "fire":
        fire_torpedo(torpedoX,torpedoY)
        torpedoY -= torpedoY_change


    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()