# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:36:03 2013

@author: Leo
"""
""
import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

TYPE_SMALL = 1
TYPE_MIDDLE = 2
TYPE_BIG = 3
items = pygame.sprite.Group()
# bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos,level):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10
        self.level = level

    def move(self):
        if self.level == 1:
            self.rect.top -= self.speed
        elif self.level == 2:
            self.rect.top -= self.speed
            self.rect.left -= self.speed/2
        elif self.level == 3:
            self.rect.top -= self.speed
            self.rect.left += self.speed/2

# collision
class Collision(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(pos, size)
        self.rect.center = pos
        self.rect.size = size
# player
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 # player sprite list
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]                      # initialize picture rectangle
        self.rect.topleft = init_pos                    # initialize rectangle upper left conrner
        self.speed = 8                                  # initialize player speed
        self.bullets = pygame.sprite.Group()            # initialize player bullet group
        self.img_index = 0                              # initialize player sprite index
        self.is_die = False                             # initialize player ishit
        self.life = 3
        self.bulletlevel = 1
        self.bomb = 0

    def shoot(self, bullet_img):
        if self.bulletlevel > 0:
            bullet = Bullet(bullet_img, self.rect.midtop, 1)
            self.bullets.add(bullet)
        if self.bulletlevel > 1:
            bullet = Bullet(bullet_img, self.rect.midtop, 2)
            self.bullets.add(bullet)
        if self.bulletlevel > 2:
            bullet = Bullet(bullet_img, self.rect.midtop, 3)
            self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

    def bomb_use(self,enemy):
        self.bomb -= 1
        for mob in enemy:
            enemy.remove(mob)

# enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 3
        self.down_index = 0
        self.die_reason = 0 #0 = player, 1=bullet

    def move(self):
        self.rect.top += self.speed
    
    def die_heart(self, heart_img):
        heart = Heart(heart_img,self.rect.topleft)
        items.add(heart)

    def die_bullet(self, bulletplus_img):
        bulletplus = BulletPlus(bulletplus_img,self.rect.topleft)
        items.add(bulletplus)

    def die_bomb(self, bomb_img):
        bomb = Bomb(bomb_img, self.rect.topleft)
        items.add(bomb)

# item - heart
class Heart(pygame.sprite.Sprite):
    def __init__(self, heart_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = heart_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 1.1

    def move(self):
        self.rect.top += self.speed

    def use(self,player):
        if player.life < 3:
            player.life += 1

# item - bulletplus
class BulletPlus(pygame.sprite.Sprite):
    def __init__(self,bulletplus_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletplus_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 1.1

    def move(self):
        self.rect.top += self.speed

    def use(self,player):
        if player.bulletlevel < 3:
            player.bulletlevel += 1

# item - bomb
class Bomb(pygame.sprite.Sprite):
    def __init__(self,bomb_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bomb_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 1.1
    
    def move(self):
        self.rect.top += self.speed
    
    def use(self,player):
        if player.bomb < 3:
            player.bomb += 1

