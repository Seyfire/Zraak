import pygame
from pygame.locals import *

import math

import constants as c
import global_vars as g
import utility as util
import SpriteStripAnim

class Player:
    speed = 4.5
    def __init__(self):
        self.rect = pygame.Rect(c.SCREENRECT.width / 2, c.SCREENRECT.height / 2, 32, 32)
        self.strips = []
        self.strips.append(SpriteStripAnim.SpriteStripAnim('assets/player.png', (0,32,32,32), 4, 1, False, c.FPS / 20))
        self.strips.append(SpriteStripAnim.SpriteStripAnim('assets/player.png', (0,64,32,32), 4, 1, True, c.FPS / 10))
        self.moving = False
        self.attacking = False
        self.imag = self.strips[0].iter()
        self.strips[1].iter()
        self.angle = 0
        self.swings = 0
        self.health = 20
        self.alive = True

    def hit(self, damage):
        if self.alive:
            self.health -= damage

    def update(self, game):
        if self.health <= 0:
            self.alive = False
            return

        # move player in directions
        xdir = (g.KEYSTATE[K_RIGHT] or g.KEYSTATE[K_d]) - (g.KEYSTATE[K_LEFT] or g.KEYSTATE[K_a])
        ydir = (g.KEYSTATE[K_DOWN] or g.KEYSTATE[K_s]) - (g.KEYSTATE[K_UP] or g.KEYSTATE[K_w])
        if (xdir or ydir):
            self.moving = True
        else:
            self.moving = False

        # step through animation frames
        if self.attacking:
            try:
                self.imag = self.strips[0].next()
            except StopIteration:
                self.imag = self.strips[0].iter().next()
                self.attacking = False
                for z in game.enemies:
                    z.hit_on_last_attack = False
        else:
            if not self.moving:
                self.imag = self.strips[int(self.moving)].iter().next()
            else:
                self.imag = self.strips[int(self.moving)].next()

        # rotate player to face mouse cursor
        self.angle = util.angle_to_coord(self.rect.center, g.MOUSEPOS) + 90
        self.imag = util.rotate_center(self.imag, self.angle)

        unit_vector = math.sqrt(xdir*xdir + ydir*ydir)
        # prevent division by zero
        if(unit_vector == 0): unit_vector = 1
        self.rect.move_ip(xdir/unit_vector*self.speed, ydir/unit_vector*self.speed)

        # constrain movement within screen borders
        self.rect = self.rect.clamp(c.SCREENRECT)

    def draw(self, screen):
        screen.blit(self.imag, self.rect.topleft)
