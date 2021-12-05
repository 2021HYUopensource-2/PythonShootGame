# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""
import time
import pygame
from sys import exit
from pygame.image import save
from pygame.locals import *
from gameRole import *
import random

def quitgame():
    pygame.quit()
    sys.exit()

def loadHighScore():
    try:
        sum = 0
        f = open("score", 'r')
        a1 = int(f.readline())
        sum += a1
        temp = a1
        a1 = a1 ^ 11498011
        a1 = 100000000 - a1
        Parity = int(f.readline())
        sum += Parity
        Parity = Parity ^ 11498011
        counter = 0
        while temp > 0:
            counter += temp % 2
            temp = temp // 2
        if Parity != counter:
            print("Cheat detected")
            #exit()
            
        a2 = int(f.readline())
        sum += a2
        temp = a2
        a2 = a2 ^ 12379813
        a2 = 100000000 - a2
        Parity = int(f.readline())
        sum += Parity
        Parity = Parity ^ 12379813
        counter = 0
        while temp > 0:
            counter += temp % 2
            temp = temp // 2
        if Parity != counter:
            print("Cheat detected")
            #exit()
            
        savedsum = str(int(f.readline()) ^ 9438121)
        savedsum.replace('0', '*')
        savedsum.replace('9', '0')
        savedsum.replace('8', '9')
        savedsum.replace('7', '8')
        savedsum.replace('6', '7')
        savedsum.replace('5', '6')
        savedsum.replace('4', '5')
        savedsum.replace('3', '4')
        savedsum.replace('2', '3')
        savedsum.replace('1', '2')
        savedsum.replace('*', '1')
        savedsum = int(savedsum) 
        if (a1 != a2) or (a1 % 1000 != 0) or (savedsum != sum):
            print("Cheat detected")
            #exit()
        f.close()
    except:
        return 0
    return a1

def saveHighScore(s):
    savedScore = loadHighScore()
    if savedScore < s:
        sum = 0
        f = open("score", 'w')
        a = 100000000 - s
        a = a ^ 11498011
        temp = a
        ParityCheck = 0
        while a > 0:
            ParityCheck += a % 2
            a = a // 2
        ParityCheck = ParityCheck ^ 11498011
        f.write(str(temp) + '\n')
        f.write(str(ParityCheck) + '\n')
        sum += temp
        sum += ParityCheck
        a = 100000000 - s
        a = a ^ 12379813
        temp = a
        ParityCheck = 0
        while a > 0:
            ParityCheck += a % 2
            a = a // 2
        ParityCheck = ParityCheck ^ 12379813
        f.write(str(temp) + '\n')
        f.write(str(ParityCheck) + '\n')
        sum += temp
        sum += ParityCheck
        sum = sum ^ 9438121
        sum = str(sum)
        sum.replace("0", "*")
        sum.replace("1", "0")
        sum.replace("2", "1")
        sum.replace("3", "2")
        sum.replace("4", "3")
        sum.replace("5", "4")
        sum.replace("6", "5")
        sum.replace("7", "6")
        sum.replace("8", "7")
        sum.replace("9", "8")
        sum.replace("*", "9")
        f.write(sum)
        f.close()
    return

def main_menu():
    screen.blit(background1, (0, 0))
    
    font = pygame.font.Font(None, 70)
    text = font.render('Aircraft War', True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery - 104
    screen.blit(text, text_rect)
    
    font = pygame.font.Font(None, 48)
    text = font.render('Press \'S\' to Start', True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(text, text_rect)
    
    menu = True
    clock = pygame.time.Clock()
    while menu:
        clock.tick(45)
        pygame.event.get()
        key_pressed = pygame.key.get_pressed()
        pygame.display.update()
        if key_pressed[K_ESCAPE]:
            menu = False
            pygame.quit()
            sys.exit()    
        if key_pressed[K_s]:
            menu = False
            play_game()  

def play_game():
    game_over_sound_isPlaying = False
    # player initialize
    player_rect = []
    player_rect.append(pygame.Rect(0, 99, 102, 126))        # Player sprite area
    player_rect.append(pygame.Rect(165, 360, 102, 126))
    player_rect.append(pygame.Rect(165, 234, 102, 126))     # Player explosion sprite area
    player_rect.append(pygame.Rect(330, 624, 102, 126))
    player_rect.append(pygame.Rect(330, 498, 102, 126))
    player_rect.append(pygame.Rect(432, 624, 102, 126))
    player_pos = [200, 600]
    player = Player(plane_img, player_rect, player_pos)
    player_collision_size = (5, 5)

    # Define the surface related parameters used by the bullet object
    bullet_rect = pygame.Rect(1004, 987, 9, 21)
    bullet_img = plane_img.subsurface(bullet_rect)

    # Define the surface related parameters used by the enemy object
    enemy1_rect = pygame.Rect(534, 612, 57, 43)
    enemy1_img = plane_img.subsurface(enemy1_rect)
    enemy1_down_imgs = []
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
    enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

    enemies1 = pygame.sprite.Group()

    # destoryed enemy list to render destruction animation
    enemies_down = pygame.sprite.Group()

    # Item - Heart
    heart_img = pygame.image.load('resources/image/heart.png')

    # Item - BulletPlus
    bulletplus_img = pygame.image.load('resources/image/bullet.png')

    # Heart UI
    heart_UI = pygame.image.load('resources/image/heart.png')

    shoot_frequency = 0
    enemy_frequency = 0

    player_down_index = 16

    score = 0
    playtime = 0
    timeChecker = time.time()

    clock = pygame.time.Clock()
    
    background1_y = 0
    background2_y = -SCREEN_HEIGHT
    background_speed = 3

    running = True
    isStop = False
    
    while running:
        # max frame = 60fps
        clock.tick(45)

        # add playtime
        playtime += time.time() - timeChecker
        timeChecker = time.time()
        
        # wait while isStop is true
        if isStop:
            score_font = pygame.font.Font(None, 36)
            score_text = score_font.render("Pause", True, (128, 128, 128))
            text_rect = score_text.get_rect()
            text_rect.centerx = round(SCREEN_WIDTH / 2)
            text_rect.centery = round(SCREEN_HEIGHT / 2)
            screen.blit(score_text, text_rect)
            pygame.display.update()
        while isStop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # resume game when Space key pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        isStop = False
            timeChecker = time.time()
        
        # bullet shoot control
        if not player.is_die:
            if shoot_frequency % 15 == 0:
                bullet_sound.play()
                player.shoot(bullet_img)
            shoot_frequency += 1
            if shoot_frequency >= 15:
                shoot_frequency = 0

        # spawn enemy
        if enemy_frequency % 50 == 0:
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
            enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
            enemies1.add(enemy1)
        enemy_frequency += 1
        if enemy_frequency >= 100:
            enemy_frequency = 0

        # bullet move, boundary check
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)

        # enemy move, boundary check
        player_collision = Collision(player_collision_size, (player.rect.centerx, player.rect.centery))
        for enemy in enemies1:
            enemy.move()
            # player collide check
            if pygame.sprite.collide_circle(enemy, player_collision):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                if player.bulletlevel > 1:
                    player.bulletlevel = 1
                if player.life > 0:
                    player.life -= 1
                if not player.life:
                    player.is_die = True
            if enemy.rect.top > SCREEN_HEIGHT:
                enemies1.remove(enemy)

        # render destruction animation
        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        for enemy_down in enemies1_down:
            enemy_down.die_reason = 1
            enemies_down.add(enemy_down)
            
        # draw background
        screen.fill(0)
        background1_y += background_speed
        background2_y += background_speed
        plus_background = 0
        if background1_y >= SCREEN_HEIGHT:
            plus_background = background1_y - SCREEN_HEIGHT
            background1_y = -SCREEN_HEIGHT + plus_background
        if background2_y >= SCREEN_HEIGHT:
            plus_background = background2_y - SCREEN_HEIGHT
            background2_y = -SCREEN_HEIGHT + plus_background
        screen.blit(background1, (0, background1_y))
        screen.blit(background2, (0, background2_y))
        
        # draw player
        if not player.is_die:
            screen.blit(player.image[player.img_index], player.rect)
            # player animation : normal
            player.img_index = shoot_frequency // 8
        else:
            # player animation : destruction
            player.img_index = player_down_index // 8
            if not game_over_sound_isPlaying:
                game_over_sound.play()
                game_over_sound_isPlaying = True
            screen.blit(player.image[player.img_index], player.rect)
            player_down_index += 1
            if player_down_index > 47:
                running = False

        # draw items
        for item in items:
            item.move()
            if pygame.sprite.collide_circle(item, player_collision):
                item.use(player)
                items.remove(item)
            if item.rect.top > SCREEN_HEIGHT:
                items.remove(item)

        # enemy animation : crash
        for enemy_down in enemies_down:
            if enemy_down.down_index == 0:
                enemy1_down_sound.play()
            if enemy_down.down_index > 7:
                if enemy_down.die_reason:
                    percent = random.randint(1,100)
                    if percent < 4:
                        enemy_down.die_heart(heart_img)
                    elif percent < 8:
                        enemy_down.die_bullet(bulletplus_img)
                enemies_down.remove(enemy_down)
                score += 1000
                continue
            screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
            enemy_down.down_index += 1
        # draw bullet, enemy
        player.bullets.draw(screen)
        enemies1.draw(screen)
        items.draw(screen)

        # draw score
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)

        # draw life
        screen.blit(heart_UI,(5,SCREEN_HEIGHT-70))
        life_font = pygame.font.Font(None, 50)
        life_text = life_font.render(str(player.life), True, (255, 0, 0))
        text_rect = life_text.get_rect()
        text_rect.topleft = [70, SCREEN_HEIGHT-60]
        screen.blit(life_text, text_rect)

        # update screen
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # pause game when Space key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    isStop = True
                
        # keyboard input event
        key_pressed = pygame.key.get_pressed()
        # If the player is hit, it has no effect
        if not player.is_die:
            # slow mode
            if key_pressed[K_LSHIFT] or key_pressed[K_RSHIFT]:
                player.speed = 4
            else:
                player.speed = 8
            # move
            if key_pressed[K_w] or key_pressed[K_UP]:
                player.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                player.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                player.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                player.moveRight()
    game_end(score, screen, game_over)


def game_end(score, screen, game_over):
    saveHighScore(score)
    screen.blit(game_over, (0, 0))

    font = pygame.font.Font(None, 48)
    text = font.render('Score: '+ str(score), True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 48)
    text = font.render('HighScore: '+ str(loadHighScore()), True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 72
    screen.blit(text, text_rect)
    
    font = pygame.font.Font(None, 48)
    text = font.render('Press \'S\' to Restart', True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 150
    screen.blit(text, text_rect)
    
    font = pygame.font.Font(None, 48)
    text = font.render('main menu = \'R\'', True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 200
    screen.blit(text, text_rect)
    
    menu = True
    clock = pygame.time.Clock()
    while menu:
        clock.tick(45)
        pygame.event.get()
        key_pressed = pygame.key.get_pressed()
        pygame.display.update()
        if key_pressed[K_ESCAPE]:
            menu = False
            pygame.quit()
            sys.exit()    
        if key_pressed[K_s]:
            menu = False
            play_game()
        if key_pressed[K_r]:
            menu = False
            main_menu() 

# initialize
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Aircraft war')

# load sound
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
game_over_sound_isPlaying = False
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# load background image
background1 = pygame.image.load('resources/image/background.png').convert()
background2 = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')

filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)

background1_y = 0
background2_y = -SCREEN_HEIGHT
background_speed = 3

# load button image
startImg = pygame.image.load('resources/image/starticon.png')
quitImg = pygame.image.load('resources/image/quiticon.png')

main_menu()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()

