#--
# tron.py
# original: 5-feb-2017/sklar
# based on Tron.java (sklar & funes, 1998)
#
# This code emulates a simple 2-player game of "Tron", inspired by the
# old 1982 Disney movie of the same name. The original version of
# this code was written in 1997-98 by Elizabeth Sklar and Pablo Funes,
# in order to conduct early human-agent experiments over the
# Internet. The game was posted on our lab's web site
# (http://demo.cs.brandeis.edu) and used to gather data that trained
# intelligent agents, controlled by genetic programs, to play the game
# better and better. The original paper on this study was:
#
# P. Funes, E. I. Sklar, H. Juille and J. Pollack (1998).
# Animal-Animat Coevolution: Using the Animal Population
# as Fitness Function. In Proceedings of the Fifth International
# Conference on Simulation of Adaptive Behavior (SAB).
#
# Two follow-on papers were later published:
#
# A. D. Blair, E. I. Sklar and P. Funes (1998). Co-evolution,
# Determinism and Robustness. In Simulated Evolution and Learning
# (SEAL), Lecture Notes in Artificial Intelligence 1585, Springer.
#
# E. I. Sklar, A. D. Blair, P. Funes and J. Pollack (1999). Training
# Intelligent Agents Using Human Internet Data. In Proceedings of the
# First Asia-Pacific Conference on Intelligent Agent Technology (IAT).
# Nominated for Best Paper Award.
#
#--

import sys
import numpy as np
import matplotlib
import time
#-for osx, this is needed to ensure events are handled correctly
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from const import Constants
from player import Player
from randm import RandomPlayer
from human import HumanPlayer
from nn import NNPlayer


#--
# define program constants
#--
#-define a 2D matrix of booleans that indicate if an agent has crossed
#-each cell in the arena (True) or not (False); initially, all cells
#-are set to False.
arena = [[ False for x in range(Constants.XMIN,Constants.XMAX)] for y in range(Constants.YMIN,Constants.YMAX) ]
#-define starting locations for player1 (agent) and player2 (human)
XSTART1 = Constants.XMAX/4
YSTART1 = Constants.YMAX/2
XSTART2 = 3*Constants.XMAX/4
YSTART2 = Constants.YMAX/2
#-define starting directions for each player
DIRECTION1 = Constants.SOUTH
DIRECTION2 = Constants.SOUTH
#-define maximum number of moves (so game doesn't hang)
MAX_MOVES = 1000000 #4096
#-define step size (in pixels) for drawing
STEP = 1
#-define size of spikes in crash star (for drawing)
CRASH_DELTA = 5
#-define length of sleep time (in fractions of a second)
SLEEP_TIME = 0.00001


#--
# markArena()
# This function marks the arena matrix according to the player's data
# that is passed as an argument to this function. The player's current
# position (x0,y0) is upated (x1,y1), based on their direction of
# travel. If the player moves to a cell that has already been marked,
# then a crash occurs. The function returns a list containing the
# current and next position of the player, their direction of travel
# and a flag indicating if a crash has occurred or not.
#--
def markArena( data ):
    # parse input argument
    x0, y0, x1, y1, direction, crash = data
    # set new position (x1,y1) based on current position (x0,y0) and
    # direction of movement
    if ( direction==Constants.SOUTH ):
        # move one step south
        y1 = y0 + STEP
        if ( y1 >= Constants.YMAX ):
            y1 = 0
            y0 = y1
    elif ( direction==Constants.NORTH ):
        # move one step north
      y1 = y0 - STEP
      if ( y1 < 0 ):
          y1 = Constants.YMAX - STEP
          y0 = y1
    elif ( direction==Constants.EAST ):
        # move one step east
        x1 = x0 + STEP
        if ( x1 >= Constants.XMAX ):
            x1 = 0
            x0 = x1
    elif ( direction==Constants.WEST ):
        # move one step west
        x1 = x0 - STEP
        if ( x1 < 0 ):
            x1 = Constants.XMAX - STEP
            x0 = x1
    else: 
        # invalid direction, so quit
        print "UH-OH!"
        sys.exit()
    # check if new position has been traversed yet or not (if it has,
    # then--oh no!--the player has crashed!)
    if ( arena[x1][y1] ):
        crash = True
    else:
        # otherwise, mark the arena to indicate that the player has
        # traversed its new current location
        arena[x1][y1] = True
    # set the return data vector
    data = [x0, y0, x1, y1, direction, crash]
    return( data )


#--
# init()
# This function is needed as an argument to the animation function
# (used below), but it does nothing (though it could, if we needed it
# to).
#--
def init():
    return


#--
# update()
# This function is invoked by the animation function and updates the
# plot while game play is active.
#--
def update( data ):
#-unpack the argument, which is a list of two lists, where each
#-sublist contains the current and next position for each player,
#-their direction of travel and a flag indicating whether they have
#-crashed or not.
    p1data = data[0]
    p2data = data[1]
    p1x0, p1y0, p1x1, p1y1, p1direction, p1crash = p1data
    p2x0, p2y0, p2x1, p2y1, p2direction, p2crash = p2data
#-initialise a counter for the number of moves in the game
    num_moves = 0
#-loop as long as game play is active (until either player crashes or
#-the maximum number of moves have been executed)
    while ( not p1crash ) and ( not p2crash ) and ( num_moves < MAX_MOVES ):
#-increment the moves counter
        num_moves = num_moves + 1
#-mark the arena with next move for each player, which also updates
#-the player's current position and their "crash" flag. unpack the
#-updated data, returned by the function.
        p1data = markArena( p1data )
        p1x0, p1y0, p1x1, p1y1, p1direction, p1crash = p1data
        p2data = markArena( p2data )
        p2x0, p2y0, p2x1, p2y1, p2direction, p2crash = p2data
        if ( p1crash ):
#-if player1 has crashed, print a message and draw crash star
            print "player1 CRASH!!"
            fig.gca().plot( [p1x1-CRASH_DELTA,p1x1+CRASH_DELTA], [p1y1-CRASH_DELTA,p1y1+CRASH_DELTA], 'r' )
            fig.gca().plot( [p1x1,p1x1], [p1y1-CRASH_DELTA, p1y1+CRASH_DELTA], 'r' )
            fig.gca().plot( [p1x1+CRASH_DELTA,p1x1-CRASH_DELTA], [p1y1-CRASH_DELTA,p1y1+CRASH_DELTA], 'r' )
            fig.gca().plot( [p1x1-CRASH_DELTA,p1x1+CRASH_DELTA], [p1y1,p1y1], 'r' )
        elif ( p2crash ):
#-if player2 has crashed, print a message and draw crash star
            print "player2 CRASH!!"
            fig.gca().plot( [p2x1-CRASH_DELTA,p2x1+CRASH_DELTA], [p2y1-CRASH_DELTA,p2y1+CRASH_DELTA], 'r' )
            fig.gca().plot( [p2x1,p2x1], [p2y1-CRASH_DELTA, p2y1+CRASH_DELTA], 'r' )
            fig.gca().plot( [p2x1+CRASH_DELTA,p2x1-CRASH_DELTA], [p2y1-CRASH_DELTA,p2y1+CRASH_DELTA], 'r' )
            fig.gca().plot( [p2x1-CRASH_DELTA,p2x1+CRASH_DELTA], [p2y1,p2y1], 'r' )
        else:
#-if nobody has crashed, update animation by drawing line segments from (x0,y0) to (x1,y1) for each player
            fig.gca().plot( [p1x0, p1x1], [p1y0, p1y1], 'm' )
            fig.gca().plot( [p2x0, p2x1], [p2y0, p2y1], 'b' )
#-update current position (x0,y0) for both players
            p1x0 = p1x1
            p1y0 = p1y1
            p2x0 = p2x1
            p2y0 = p2y1
#-determine where next direction should be for each player
            p1direction = player1.whereDoIGo( p1x0, p1y0, arena )
            p2direction = player2.whereDoIGo( p2x0, p2y0, arena )
#-sleep for a fraction of a second to allow human player to comprehend what is happening
            plt.pause( SLEEP_TIME )
#-encode each player's updated data for the next iteration of the game play loop
        p1data = [p1x0, p1y0, p1x1, p1y1, p1direction, p1crash]
        p2data = [p2x0, p2y0, p2x1, p2y1, p2direction, p2crash]
#-did we stop because we hit max moves?
    if ( num_moves >= MAX_MOVES ):
        print 'early termination: max_moves met (' + str( MAX_MOVES ) + ')'
#-done playing!
    return

def play_bash(data):
    #-unpack the argument, which is a list of two lists, where each
#-sublist contains the current and next position for each player,
#-their direction of travel and a flag indicating whether they have
#-crashed or not.
    p1data = data[0]
    p2data = data[1]
    p1x0, p1y0, p1x1, p1y1, p1direction, p1crash = p1data
    p2x0, p2y0, p2x1, p2y1, p2direction, p2crash = p2data
#-initialise a counter for the number of moves in the game
    num_moves = 0
#-loop as long as game play is active (until either player crashes or
#-the maximum number of moves have been executed)
    while ( not p1crash ) and ( not p2crash ) and ( num_moves < MAX_MOVES ):
#-increment the moves counter
        num_moves = num_moves + 1
#-mark the arena with next move for each player, which also updates
#-the player's current position and their "crash" flag. unpack the
#-updated data, returned by the function.
        p1data = markArena( p1data )
        p1x0, p1y0, p1x1, p1y1, p1direction, p1crash = p1data
        p2data = markArena( p2data )
        p2x0, p2y0, p2x1, p2y1, p2direction, p2crash = p2data
        if ( p1crash ):
#-if player1 has crashed, print a message and draw crash star
            print "player1 CRASH!!"
        elif ( p2crash ):
#-if player2 has crashed, print a message and draw crash star
            print "player2 CRASH!!"
        else:
#-if nobody has crashed, update animation by drawing line segments from (x0,y0) to (x1,y1) for each player
            
#-update current position (x0,y0) for both players
            p1x0 = p1x1
            p1y0 = p1y1
            p2x0 = p2x1
            p2y0 = p2y1
#-determine where next direction should be for each player
            p1direction = player1.whereDoIGo( p1x0, p1y0, arena )
            p2direction = player2.whereDoIGo( p2x0, p2y0, arena )
#-sleep for a fraction of a second to allow human player to comprehend what is happening

#-encode each player's updated data for the next iteration of the game play loop
        p1data = [p1x0, p1y0, p1x1, p1y1, p1direction, p1crash]
        p2data = [p2x0, p2y0, p2x1, p2y1, p2direction, p2crash]
#-did we stop because we hit max moves?
    if ( num_moves >= MAX_MOVES ):
        print 'early termination: max_moves met (' + str( MAX_MOVES ) + ')'
#-done playing!
    return


#--
# play() function
# starts the animation loop (i.e., game play)
#--
def play():
#-start animation
    ani = animation.FuncAnimation( fig, # the plot figure
                                   update, # the function to be called in each frame
                                   data, # the data to be passed to the update() function (each frame)
                                   init_func=init, # function to be called once, before the first frame
                                   interval=10, # delay between frames, in milliseconds
                                   repeat=False # indicates whether animation should repeat when sequence of frames is done
                                   )
#-show the plot where the animation is displayed
    plt.show()


#--
# main starts here
#--

#-initialise lists of paramters for player1 (agent) and player2 (human)
#-data is in the following format:
#- [x0, y0, x1, y1, direction, crash]
p1data = [XSTART1, YSTART1, XSTART1, YSTART1, DIRECTION1, False]
p2data = [XSTART2, YSTART2, XSTART2, YSTART2, DIRECTION2, False]
data = [[p1data, p2data]]
#-open log files for storing player moves
now = time.time()
try:
    filename = 'p1-log-%d.dat' % now
    p1log = open( filename, 'w' )
    filename = 'p2-log-%d.dat' % now
    p2log = open( filename, 'w' )
except IOError as iox:
    print 'error opening player log file [' + filename + ']: ' + str( iox )
    sys.exit()
#-initialise player objects
#player1 = Player( 1 )
#player1 = RandomPlayer( 1 )
player1 = NNPlayer( 1, Constants.TRAINED_NN_PATH + 'nn-online-steps100.1', p1log )
player2 = NNPlayer( 2, Constants.TRAINED_NN_PATH + 'nn-online-steps1000.2', p2log )
#player2 = HumanPlayer( 2 )
#-mark cells in arena where each player starts
arena[XSTART1][YSTART1] = True
arena[XSTART2][YSTART2] = True
#-initialise matplotlib figure for displaying animation
fig = plt.figure()
fig.hold( True )
fig.gca().set_xlim( Constants.XMIN, Constants.XMAX )
fig.gca().set_ylim( Constants.YMIN, Constants.YMAX )
fig.gca().set_xticklabels( '' )
fig.gca().set_yticklabels( '' )
fig.gca().set_axis_bgcolor( 'k' )
#-initialise event handler to be called on "key release" events
if ( player1.mode == "human" ):
    cid = fig.canvas.mpl_connect( 'key_release_event', player1.on_key )
if ( player2.mode == "human" ):
    cid = fig.canvas.mpl_connect( 'key_release_event', player2.on_key )
#-start animation loop (i.e., game play)
play()

# bash_mode (for generating data)
# play_bash(data[0])

#-close log files
p1log.close()
p2log.close()
