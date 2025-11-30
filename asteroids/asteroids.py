import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

import warnings

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API"
)


import pygame
import numpy as np
import math
import random

pygame.init()
#-------os----------:

pasta = os.getcwd()

arquivo = os.path.join(pasta, "max_score.bin")

icon = pygame.image.load('imgs\\icon.png')

pygame.display.set_caption('Space Shooter')

asteroids_imgs = [
    pygame.image.load('imgs/asteroid0.png'),
    pygame.image.load('imgs/asteroid1.png'),
    pygame.image.load('imgs/asteroid2.png')
    ]


player_img = pygame.image.load('imgs\\shooter.png')
player_img = pygame.transform.scale_by(player_img, 0.1)

gameover = pygame.image.load('imgs\\gameover.png')

game_o = False

shoot = False

on = True

# ----display-----:
w, h = 650, 650
screen = pygame.display.set_mode((w, h))
pygame.display.set_icon(icon)


# //----------------Game_Settings-----------------------------:
n_of_asteroids = 15
asteroid_speed = 0.1
life = 5
max_score = 0

font = pygame.font.Font(".fonts\\ARCADE.otf", 70)
text = font.render('Hello', False, (255, 255, 255))


#----------file_handling-----------:        #aka boring stuff
if not os.path.exists(arquivo):

    with open(arquivo, "wb") as f:
        f.write((0).to_bytes(4, "big"))

# Leitura
with open(arquivo, "rb") as f:
    data = f.read(4)  # ler 4 bytes
    max_score = int.from_bytes(data, "big")
os.system(f'attrib +r "{arquivo}"')
#...........................................................................................................

#-------------funcions-----:

def blit_rotate_center(s, img, top_l, angle, blit=True):
    rotated_img = pygame.transform.rotate(img, angle)
    new_rect = rotated_img.get_rect(center=img.get_rect(topleft=top_l).center)
    if blit:
        s.blit(rotated_img, new_rect.topleft)
    return new_rect.center

def reset_game():
    global player1, bullet, asteroids, shoot, score, life, game_o
    player1 = shooter()
    bullet = Bullet()
    asteroids = [Asteroid() for _ in range(n_of_asteroids)]
    shoot = False
    score = 0
    life = 5
    game_o = False

#-----------classes----------this took a while:

class shooter:
    def __init__(self):
        self.x = w//2
        self.y = h//2
        self.speed = 0
        self.x_speed = 0
        self.y_speed = 0
        self.dir = 10
        self.rad = math.radians(self.dir)
        self.acc = 0.0005
        self.hitbox = pygame.Rect(self.x, self.y, round(player_img.get_width()), round(player_img.get_height()))

    def draw(self):
        if self.speed != 0:
            blit_rotate_center(screen, player_img,(player1.x, player1.y), -player1.dir)
        h = pygame.Rect(self.x, self.y, 5, 5)
        self.hitbox = pygame.Rect(self.x, self.y, round(player_img.get_width()), round(player_img.get_height()))
        

    def move_f(self):
        self.rad = math.radians(self.dir)
        self.x += self.x_speed
        self.y += self.y_speed
        self.x_speed = math.cos(self.rad) * self.speed
        self.y_speed = math.sin(self.rad) * self.speed

    def slow_down(self):
        if self.speed > 0:
            self.speed -= self.acc * 2

    def accelerate(self):
        if self.speed < 2:
            self.speed += self.acc

    def tp(self):
        if self.x < 0:
            self.x = w
        elif self.x > w:
            self.x = 0
        elif self.y < 0:
            self.y = h
        elif self.y > h:
            self.y = 0

    def get_tip_pos(self):
        img_w, img_h = player_img.get_size()
        dx = img_w / 2
        dy = 0 
        center = blit_rotate_center(
            screen, player_img, (player1.x, player1.y), -player1.dir, blit=False)
        tip_x = center[0] + dx * math.cos(self.rad) - dy * math.sin(self.rad)
        tip_y = center[1] + dx * math.sin(self.rad) + dy * math.cos(self.rad)
        return tip_x, tip_y


player1 = shooter()

score = 0
class Bullet:
    def __init__(self):
        self.x, self.y = player1.get_tip_pos()
        self.rad = math.radians(player1.dir)
        self.x_speed = math.cos(self.rad) * 2
        self.y_speed = math.sin(self.rad) * 2
        self.hitbox = bullet = pygame.Rect(self.x, self.y, 5, 5)
        
    def move_f(self):
        self.x_speed = math.cos(self.rad) * 2
        self.y_speed = math.sin(self.rad) * 2
        self.x += self.x_speed
        self.y += self.y_speed
        self.hitbox = bullet = pygame.Rect(self.x, self.y, 5, 5)

    def draw(self):
        bullet = pygame.Rect(self.x, self.y, 5, 5)
        pygame.draw.rect(screen, (255, 255, 255), bullet)

    def d_off_screen(self):
        if self.x < 0 or self.x > w or self.y < 0 or self.y > h:
            return True
        return False




class Asteroid:
    def __init__(self):
        self.size = random.uniform(0.1, 0.5)
        self.x, self.y, self.x_speed, self.y_speed = random.randint(0, w), random.randint(0, h), random.uniform(-asteroid_speed, asteroid_speed), random.uniform(-asteroid_speed, asteroid_speed)
        self.image = pygame.transform.scale_by(random.choice(asteroids_imgs), self.size)
        self.hitbox = pygame.Rect(self.x, self.y, round(self.image.get_width()), round(self.image.get_height()))
    def spawn(self):

        self.size = random.uniform(0.1, 0.5)
        self.image = pygame.transform.scale_by(random.choice(asteroids_imgs), self.size)

        side = random.choice(["top", "bottom", "left", "right"])
            
        if side == "top":
            self.x = random.randint(0, w)
            self.y = 0
        elif side == "bottom":
            self.x = random.randint(0, w)
            self.y = h
        elif side == "left":
            self.x = 0
            self.y = random.randint(0, h)
        else:  # right
            self.x = w
            self.y = random.randint(0, h)
            
        self.x_speed = random.uniform(-asteroid_speed, asteroid_speed)
        self.y_speed = random.uniform(-asteroid_speed, asteroid_speed)


    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        self.hitbox = pygame.Rect(self.x, self.y, round(self.image.get_width()), round(self.image.get_height()))
        self.x += self.x_speed
        self.y += self.y_speed
        if self.x < 0 or self.x > w:
            self.spawn()
        elif self.y < 0 or self.y > h:
            self.spawn()

bullet = Bullet()



asteroids = []
for i in range(n_of_asteroids):      #spawn asteroids
    asteroids.append(Asteroid())

#---main loop---:

while on:
    if game_o:
        #---------if you can't play a simple game this happens--------:
        screen.fill((0, 0, 10))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    life = 5
                    reset_game()
        
        screen.blit(gameover, (0, 0))
        text = font.render((f'max score: {max_score}'), False, (255, 5, 5))
        screen.blit(text, (0, -25))
        pygame.display.flip()
    else:

        #----------------draw_things-------------:
        screen.fill((0, 0, 10))
        text = font.render((f'score: {score}         health:{life}'), False, (255, 255, 255))
        screen.blit(text, (0, -25))
        #----------asteroids----------:
                                                #this part took 2h but lets pretend it didn't 
        for asteroid in asteroids:
            if asteroid.hitbox.colliderect(bullet.hitbox): 
                asteroid.spawn()
                score += int(asteroid.size*100)
            if asteroid.hitbox.colliderect(player1.hitbox):
                life -= 1
                asteroid.spawn()
            if bullet.hitbox.colliderect(asteroid.hitbox):
                shoot = False
            asteroid.draw()

        #bullets         :cool stuf right here:

        if not bullet.d_off_screen() and shoot:
            bullet.move_f()
            bullet.draw()
        else:
            shoot = False
        #event_handeling: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
        #------key presses----:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not shoot:
                bullet = Bullet()
                shoot = True
        if keys[pygame.K_UP]:
            player1.accelerate()
        if not keys[pygame.K_UP]:
            player1.slow_down()
        if keys[pygame.K_LEFT]:
            player1.dir -= 0.2
        elif keys[pygame.K_RIGHT]:
            player1.dir += 0.2
        #-------idk what to call this---:
        player1.move_f()
        player1.tp()
        player1.draw()
        #score and lives:
        if life <= 0:
            game_o = True
        if score >= max_score:
            max_score = score

        pygame.display.flip()

#save max score:


os.makedirs(pasta, exist_ok=True)
os.system(f'attrib -r "{arquivo}"')
max_score = max_score.to_bytes(4, 'big')                        #more boring stuff
with open(arquivo, "wb") as f:
    f.write(max_score)
    
os.system(f'attrib +r "{arquivo}"')


#it's currently 23:21
#now it´s midnight