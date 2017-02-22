#--
# humn.py
# original: 12-feb-2017/sklar
# based on Tron HumanPlayer.java (sklar & funes, 1998)
#--

from const import Constants
from player import Player


class HumanPlayer( Player ):
    #--
    # constructor
    #--
    def __init__( self, number ):
        super( HumanPlayer, self ).__init__( number )
        self.mode = "human"
        self.direction = Constants.SOUTH
        self.new_direction = Constants.SOUTH
        self.move = Constants.MOVE_STRAIGHT
    #--
    # on_key()
    # This function is an event handler that is called when "key release"
    # events occur. If an arrow key is pressed, then the direction of
    # travel for player2 is changed accordingly.
    # Note that key events are opposite from what we expect for north/south.
    #--
    def on_key( self, event ):
        print( 'you pressed: ', event.key, event.xdata, event.ydata )
        if ( event.key == 'up' ):
            self.new_direction = Constants.SOUTH
        elif ( event.key == 'down' ):
            self.new_direction = Constants.NORTH
        elif ( event.key == 'left' ):
            self.new_direction = Constants.WEST
        elif ( event.key == 'right' ):
            self.new_direction = Constants.EAST
    #--
    # whereDoIGo()
    #--
    def whereDoIGo( self, x, y, arena ):
        #-evaluate sensors
        self.updateSensors( x, y, arena )
        #-determine new direction of travel
        self.move = Constants.MOVE_STRAIGHT
        if ( self.direction == Constants.SOUTH ):
            if ( self.new_direction == Constants.WEST ):
                self.move = Constants.MOVE_RIGHT_TURN
            elif ( self.new_direction == Constants.EAST ):
                self.move = Constants.MOVE_LEFT_TURN
        elif ( self.direction == Constants.NORTH ):
            if ( self.new_direction == Constants.WEST ):
                self.move = Constants.MOVE_LEFT_TURN
            elif ( self.new_direction == Constants.EAST ):
                self.move = Constants.MOVE_RIGHT_TURN
        elif ( self.direction == Constants.WEST ):
            if ( self.new_direction == Constants.SOUTH ):
                self.move = Constants.MOVE_LEFT_TURN
            elif ( self.new_direction == Constants.NORTH ):
                self.move = Constants.MOVE_RIGHT_TURN
        elif ( self.direction == Constants.EAST ):
            if ( self.new_direction == Constants.SOUTH ):
                self.move = Constants.MOVE_RIGHT_TURN
            elif ( self.new_direction == Constants.NORTH ):
                self.move = Constants.MOVE_LEFT_TURN
        self.direction = self.new_direction
        #-output sensors and move
        print self
        return( self.direction )
