import asyncio
import pygame
import os

pygame.init()

WIN_HEIGHT = 500
WIN_WIDTH = 800
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Space 1v1")
FPS = 60
VEL = 8
BULLET_VEL = 10
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.Font("gangofthree.ttf", 40)


# Characters
spaceship1 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets','spaceship_red.png')), (50, 50)), 90 )
spaceship2 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets','spaceship_yellow.png')), (50, 50)), -90)
# Background
background = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')), (WIN_WIDTH,WIN_HEIGHT))
# Sound
shoot_sound = pygame.mixer.Sound(os.path.join('Assets', 'shot.mp3'))
death_sound = pygame.mixer.Sound(os.path.join('Assets', 'death.mp3'))
# Tick Rate
clock = pygame.time.Clock()

def draw(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    win.blit(background, (0,0))

    red_health_text = HEALTH_FONT.render("Red Health:" + str(red_health), 1, (255,255,255))
    yellow_health_text = HEALTH_FONT.render("Yellow Health:" + str(yellow_health), 1, (255,255,255))
    win.blit(yellow_health_text, (WIN_WIDTH - yellow_health_text.get_width() - 10, 10))
    win.blit(red_health_text, (10, 10))

    win.blit(spaceship1, (red.x, red.y))
    win.blit(spaceship2, (yellow.x, yellow.y))
    

    for bullet in red_bullets:
        pygame.draw.rect(win, (255,0,0), bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(win, (255,255,0), bullet)
    



    pygame.display.update()

def move_red(red):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_w] and red.y - VEL > 0 :
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL + red.height <=  WIN_HEIGHT:
        red.y += VEL
    if keys_pressed[pygame.K_d] and red.x + VEL + red.width <= WIN_WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_a] and red.x - VEL >= 0:
        red.x -= VEL
def move_yellow(yellow):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys[pygame.K_DOWN] and yellow.y + VEL + yellow.height <= WIN_HEIGHT :
        yellow.y += VEL
    if keys[pygame.K_RIGHT] and yellow.x + VEL + yellow.width <= WIN_WIDTH:
        yellow.x += VEL
    if keys[pygame.K_LEFT] and yellow.x - VEL >= 0:
        yellow.x -= VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIN_WIDTH:
            yellow_bullets.remove(bullet)           

# Main Loop
red = pygame.Rect(100, 300 , 50 , 50)
yellow = pygame.Rect(700, 300 , 50 , 50)

red_bullets = []
yellow_bullets = []
yellow_health = 20
red_health = 20 
keys_pressed = pygame.key.get_pressed()


run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and len(red_bullets) < MAX_BULLETS:
                pygame.mixer.Sound.play(shoot_sound)
                bullet = pygame.Rect(red.x + red.width , red.y + red.height//2 - 2, 10, 5)
                red_bullets.append(bullet)

            if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                pygame.mixer.Sound.play(shoot_sound)
                bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                yellow_bullets.append(bullet)

        if event.type == RED_HIT:
            yellow_health -= 1
        
        if event.type == YELLOW_HIT:
            red_health -= 1

    if red_health <= 0:
        pygame.mixer.Sound.play(death_sound)
        win.fill((0,0,0))
        font = pygame.font.Font("gangofthree.ttf", 50)
        text = "YELLOW WINS!!"
        text_surface = font.render(text, 1, (255,255,255))
        win.blit(font.render(text , 1 , (255,255,255)), (WIN_WIDTH//2 - text_surface.get_width() // 2 , WIN_HEIGHT//2 - text_surface.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(1000)
        run = False

    if yellow_health <= 0:
        pygame.mixer.Sound.play(death_sound)
        win.fill((0,0,0))
        font = pygame.font.Font("gangofthree.ttf", 50)
        text = "RED WINS!!"
        text_surface = font.render(text, 1, (255,255,255))
        win.blit(font.render(text, 1 , (255,255,255)),(WIN_WIDTH//2 - text_surface.get_width() // 2, WIN_HEIGHT// 2 - text_surface.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(1000)
        run = False
  


    handle_bullets(red_bullets, yellow_bullets, red, yellow)

    draw(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    move_red(red)  
    move_yellow(yellow)





pygame.quit()


