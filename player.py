#--
# player.py
# original: 12-feb-2017/sklar
# based on Tron Player.java (sklar & funes, 1998)
#--

import random
from const import Constants


class Player( object ):
    #--
    # constructor
    #--
    def __init__( self, number ):
        self.mode = "generic"
        self.playerNum = number
        self.direction = Constants.SOUTH
        self.move = Constants.MOVE_STRAIGHT
        self.skipCount = 0
        self.numSensors = 8
        self.sensors = [0 for i in range(0,self.numSensors)]
    #--
    # print representative value
    #--
    def __str__( self ):
        mystr = 'player ' + str( self.playerNum ) + ' sensors ' 
        for i in range(0,self.numSensors):
            mystr = mystr + str( self.sensors[i] ) + ' '
        mystr = mystr + 'move ' + Constants.MOVE_NAMES[self.move+1]
        return( mystr )
    #--
    # sense()
    # evaluates one sensor by counting the number of open pixels from
    # (x,y) position by (u,v) amounts
    #--
    def sense( self, x, y, u, v, arena ):
        i = 0
        foundWall = False
        while ( not foundWall ):
            x += u
            if ( x == Constants.XMAX ):
                x = Constants.XMIN
            elif ( x == Constants.XMIN-1 ):
                x = Constants.XMAX - 1
            y = y + v
            if ( y == Constants.YMAX ):
                y = Constants.YMIN
            elif ( y == Constants.YMIN-1 ):
                y = Constants.YMAX - 1
            if ( arena[x][y] ):
                foundWall = True
            i = i + 1
        return( float( Constants.XMAX - i ))
    #--
    # updateSensors()
    # evaluates all 8 sensors
    # sensors:
    #   5 4 3
    #    \|/
    #   6- -2
    #    /|\
    #   7 0 1
    #--
    def updateSensors( self, x, y, arena ):
        i = 2 * self.direction
        self.sensors[(0-i+8)%8] = self.sense( x, y,  0,  1, arena )
        self.sensors[(1-i+8)%8] = self.sense( x, y,  1,  1, arena )
        self.sensors[(2-i+8)%8] = self.sense( x, y,  1,  0, arena )
        self.sensors[(3-i+8)%8] = self.sense( x, y,  1, -1, arena )
        self.sensors[(4-i+8)%8] = self.sense( x, y,  0, -1, arena )
        self.sensors[(5-i+8)%8] = self.sense( x, y, -1, -1, arena )
        self.sensors[(6-i+8)%8] = self.sense( x, y, -1,  0, arena )
        self.sensors[(7-i+8)%8] = self.sense( x, y, -1,  1, arena )
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
            # if I weren't the generic player, then I'd do something
            # in here to determine if I should change my direction...
            #-output sensors and move
            print self
        return( self.direction )
