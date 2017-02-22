#--
# rndm.py
# original: 12-feb-2017/sklar
# based on Tron RandomPlayer.java (sklar & funes, 1998)
#--

import random
from const import Constants
from player import Player


class RandomPlayer( Player ):
    #--
    # constructor
    #--
    def __init__( self, number ):
        super( RandomPlayer, self ).__init__( number )
        self.mode = "random"
        self.direction = random.randint( 0, 3 )
        self.move = random.randint( 0, 2 ) - 1
    #--
    # whereDoIGo()
    # This picks a direction for a player to travel in, based on the
    # behaviour mode of the player. The direction is one of the four
    # compass directions defined above.
    # The randint(0,2) function returns a value between (0,2), inclusive.
    #--
    def whereDoIGo( self, x, y, arena ):
        if ( self.skipCount < Constants.SKIP_STEPS ):
            self.skipCount = self.skipCount + 1
        else:
            self.skipCount = 0
            #-evaluate sensors
            self.updateSensors( x, y, arena )
            #-determine new direction of travel
            self.move = random.randint( 0, 2 ) - 1
            self.direction = ( self.direction + self.move + 4 ) % 4
            #-output sensors and move
            print self
        return( self.direction )
