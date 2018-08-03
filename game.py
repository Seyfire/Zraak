#!/usr/bin/python3
import pygame
from pygame.locals import *

import math
import time
import random, os.path

import player
import constants as c
import CustomGameScript
import global_vars as g
import utility as util
import zombie

main_dir = os.path.split(os.path.abspath(__file__))[0]

class Game:
    def __init__(self):
        # initialize the pygame module
        pygame.init()
        logo = pygame.image.load("assets/logo.jpeg")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Swords n Zombies")

        # create a surface on screen that has the size of 800 x 600
        self.screen = pygame.display.set_mode((c.SCREENRECT.width,c.SCREENRECT.height))
        pygame.display.flip()

        # define a variable to control the main loop
        self.running = True

        #create the background, tile the bgd image
        bgdtile = load_image('assets/bg-grass.png').convert()
        self.background = pygame.Surface(c.SCREENRECT.size)
        for x in range(0, c.SCREENRECT.width, bgdtile.get_width()):
            self.background.blit(bgdtile, (x, 0))
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()
        
        # create player and list of enemies
        self.player = player.Player()
        self.enemies = []
        
        # scoring
        self.score = 0
        
        # the "script" file for writing in custom game things
        self.customGameScript = CustomGameScript.CustomGameScript(self)
    
    #############################
    #       Main Game Loop      #
    #############################
    def Update(self, dt):
        # update keyboard state and mouse position
        g.KEYSTATE = pygame.key.get_pressed()
        g.MOUSEPOS = pygame.mouse.get_pos()
        if g.KEYSTATE[pygame.K_c]:
            self.AddEnemy(random.randint(0, c.SCREENRECT.width), random.randint(0, c.SCREENRECT.height))
        
        # update player
        self.player.update(self)
        
        # calculates the hitbox in front of player
        if self.player.attacking:
            hang = self.player.angle + 30 - 90
            lang = self.player.angle - 30 - 90
            triangle = [(self.player.rect.centerx, self.player.rect.centery), (c.PLAYERREACH * math.cos(math.pi/180*hang) + self.player.rect.centerx, self.player.rect.centery - c.PLAYERREACH * math.sin(math.pi / 180 * hang)), (c.PLAYERREACH * math.cos(math.pi/180*lang) + self.player.rect.centerx, self.player.rect.centery - c.PLAYERREACH * math.sin(math.pi / 180 * lang))]
            # call hit() on zombies that are in range
            for z in self.enemies:
                if util.point_in_triangle((z.rect.centerx, z.rect.centery), triangle):
                    z.hit()
        
        # update enemies
        for z in self.enemies:
            z.update(self)
        self.enemies = [enemy for enemy in self.enemies if not enemy.destroyed]

        # call the custom game script's update function
        self.customGameScript.update()
    
    def Draw(self):
        # call draw on all objects
        self.screen.blit(self.background, (0,0))
        for z in self.enemies:
            z.draw(self.screen)
        self.player.draw(self.screen)
        
        # draw HUD
        self.DrawHUD()
        
        pygame.display.flip()
       
    def DrawHUD(self):
        pygame.draw.rect(self.screen, [255,255,255], Rect(0,0,c.SCREENRECT.width,50))
        if pygame.font:
            # choose font
            font = pygame.font.Font(None, 36)
            
            # setup texts to display
            # score
            scoretext = font.render("Score: " + str(self.score), 10, (10, 10, 10))
            scoretextpos = scoretext.get_rect(topleft=self.screen.get_rect().topleft)
            # enemies
            enemyCountText = font.render("Enemies remaining: " + str(len(self.enemies)), 10, (10,10,10))
            enemyCountTextPos = enemyCountText.get_rect(topright=self.screen.get_rect().topright)
            # player health
            healthText = font.render("Health: " + str(self.player.health), 10, (10,10,10))
            healthTextPos = healthText.get_rect(topleft=scoretext.get_rect().bottomleft)
            # Game Over text
            gameoverText = pygame.font.Font(None, 144).render("GAME OVER!", 10, (255,10,10))
            gameoverTextPos = gameoverText.get_rect(center = self.screen.get_rect().center)
            
            # display texts
            self.screen.blit(scoretext, scoretextpos)
            self.screen.blit(enemyCountText, enemyCountTextPos)
            self.screen.blit(healthText, healthTextPos)
            if(self.player.alive == False):
                self.screen.blit(gameoverText, gameoverTextPos)

    def main(self):
        # game clock
        clock = pygame.time.Clock()
        # main loop
        while self.running:
            # event handling, gets all event from the eventqueue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.attacking = True
                    self.player.swings += 1

            self.Update(clock.tick(c.FPS))
            if g.KEYSTATE[pygame.K_ESCAPE]:
                self.running = False
            self.Draw()
    
    def AddEnemy(self, x, y, health=3, score=100, damage=1, reach=5):
        newEnemy = zombie.Zombie(x,y,health,score,damage,reach)
        self.enemies.append(newEnemy)
        return newEnemy



########################################
#       Other random functions         #
########################################


def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    game = Game()
    # call the main function
    game.main()
