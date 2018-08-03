import pygame
from pygame.locals import *

import math
import numpy

import constants as c
import global_vars as g
import utility as util
import SpriteStripAnim

class Zombie:
    speed = 3
    destroyed = False
    hit_on_last_attack = False

    def hit(self):
        if not self.hit_on_last_attack:
            self.hit_on_last_attack = True
            self.health -= 1

    def __init__(self, x, y, health, score, damage, reach):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.strip = SpriteStripAnim.SpriteStripAnim('assets/zombie.png', (0,0,32,32), 4, 1, True, c.FPS / 10)
        self.imag = self.strip.iter()
        self.health = health
        self.score = score
        self.ticks_to_hit = c.FPS
        self.current_ticks_to_hit = 0
        self.damage = damage
        self.reach = reach

    def update(self, game):
        # check if enemy is dead
        if self.health <= 0:
            self.destroyed = True
            game.score += self.score

        # caluclate distance to player
        dx = self.rect.centerx - game.player.rect.centerx
        dy = self.rect.centery - game.player.rect.centery
        dist = math.sqrt(dx * dx + dy * dy)
        if dist <= self.reach:
            if self.current_ticks_to_hit <= 0:
                game.player.hit(self.damage)
                self.current_ticks_to_hit = self.ticks_to_hit
            else:
                self.current_ticks_to_hit -= 1

        # update frame of animation
        self.imag = self.strip.next()

        # rotate to view player
        angle = util.angle_to_coord(self.rect.center, game.player.rect.center) + 90
        self.imag = util.rotate_center(self.imag, angle)
        dx = game.player.rect.centerx - self.rect.centerx
        dy = game.player.rect.centery - self.rect.centery
        normalized_dist = math.sqrt(dx*dx + dy*dy)
        if normalized_dist == 0:
            normalized_dist = 1

        # walk towards player
        self.rect.move_ip(dx / normalized_dist*self.speed, dy / normalized_dist*self.speed)



        # constrain movement within screen borders
        self.rect = self.rect.clamp(c.SCREENRECT)

    def draw(self, screen):
        screen.blit(self.imag, self.rect.topleft)
