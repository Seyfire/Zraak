import constants as c
import global_vars as g

class CustomGameScript:
    time = 0
#####################################################
#   Initialization                                  #
#   ---------------------------------------------   #
#   This function runs only once at the very        #
#       beginning of the game.                      #
#####################################################
    def __init__(self, main):
        self._game = main
        game = self._game
        
        # start coding down here
        game.AddEnemy(120,120)

#####################################################
#   Update function                                 #
#   ---------------------------------------------   #
#   This function runs every frame!                 #
#   Think of it as a repeat block.                  #
#####################################################
    def update(self):
        game = self._game
        self.time += 1
        
        # start coding down here
        
