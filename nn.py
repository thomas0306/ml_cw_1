#--
# nn.py
# original: 12-feb-2017/sklar
# based on Tron NNPlayer.java (sklar & funes, 1998)
#--

import sys
import re
import math
import random
from const import Constants
from player import Player
from functools import partial


class NNPlayer( Player ):
    #--
    # constructor
    #--
    def __init__( self, number, winfile, logfile ):
        super( NNPlayer, self ).__init__( number )
        self.winfile = winfile # save name of input weights file
        self.logfile = logfile # save file pointer for player log file
        self.mode = "nn"
        self.direction = Constants.SOUTH
        self.move = Constants.MOVE_STRAIGHT
        if ( len(self.winfile) > 0 ):
            self.readNetwork()
        else:
            self.setRandom()
        self.learningRate = 0.001
        self.momentum = 0.9
    #--
    # setRandom()
    # set all weights to Gaussian random values
    #--
    def setRandom( self ):
        #-set network layer sizes
        self.numInput  = 8
        self.numHidden = 5
        self.numOutput = 3
        #-allocate space for network content and weights
        self.x_in    = [0.0 for i in range(0,self.numInput)]
        self.hid     = [0.0 for i in range(0,self.numHidden)]
        self.hidSum  = [0.0 for i in range(0,self.numHidden)]
        self.out     = [0.0 for i in range(0,self.numOutput)]
        self.outBias = [0.0 for i in range(0,self.numOutput)]
        self.hidBias = [0.0 for i in range(0,self.numHidden)]
        self.outHid  = [[0.0 for j in range(0,self.numOutput)] for i in range(0,self.numHidden)]
        self.hidIn   = [[0.0 for j in range(0,self.numHidden)] for i in range(0,self.numInput)]
        #-set weights randomly
        for i in range(0,self.numHidden):
            self.hidBias[i] = random.gauss( 0.0, 1.0 )
            for j in range(0,self.numInput):
                self.hidIn[j][i] = random.gauss( 0.0, 1.0 )
        for i in range(0,self.numOutput):
            self.outBias[i] = random.gauss( 0.0, 1.0 )
            for j in range(0,self.numHidden):
                self.outHid[j][i] = random.gauss( 0.0, 1.0 )
    #--
    # readNetwork()
    # reads in network parameters and weights from a file
    #--
    def readNetwork( self ):
        try:
            f = open( self.winfile, 'r' )
            #-1st line is number of input nodes
            line = re.split( '[ \t]', f.readline().strip() )
            self.numInput = int( line[1] )
            #-2nd line is number of hidden nodes
            line = re.split( '[ \t]', f.readline().strip() )
            self.numHidden = int( line[1] )
            #-3rd line is number of output nodes
            line = re.split( '[ \t]', f.readline().strip() )
            self.numOutput = int( line[1] )
            #-4th line is blank
            line = f.readline().strip()
            #-allocate space for network content and weights
            self.x_in    = [0.0 for i in range(0,self.numInput)]
            self.hid     = [0.0 for i in range(0,self.numHidden)]
            self.hidSum  = [0.0 for i in range(0,self.numHidden)]
            self.out     = [0.0 for i in range(0,self.numOutput)]
            self.outBias = [0.0 for i in range(0,self.numOutput)]
            self.hidBias = [0.0 for i in range(0,self.numHidden)]
            self.outHid  = [[0.0 for j in range(0,self.numOutput)] for i in range(0,self.numHidden)]
            self.hidIn   = [[0.0 for j in range(0,self.numHidden)] for i in range(0,self.numInput)]
            #-read weights from file
            for i in range(0,self.numHidden):
                self.hidBias[i] = float( f.readline().strip() )
                for j in range(0,self.numInput):
                    self.hidIn[j][i] = float( f.readline().strip() )
                f.readline() # skip blank line
            for i in range(0,self.numOutput):
                self.outBias[i] = float( f.readline().strip() )
                for j in range(0,self.numHidden):
                    self.outHid[j][i] = float( f.readline().strip() )
                f.readline() # skip blank line
            f.close()
        except IOError as iox:
            print 'error opening file [' + filename + ']: ' + str( iox )
            sys.exit()
    #--
    # printNetwork()
    # prints network parameters and weights to a file or stdout.
    #--
    def printNetwork( self, woutfile ):
        if ( len( woutfile ) > 0 ):
            try:
                f = open( woutfile, 'w' )
            except IOError as iox:
                print 'error opening output weights file [' + woutfile + ']: ' + str( iox )
                sys.exit()
        else:
            f = sys.stdout
        f.write( 'uNumInput ' + str(self.numInput) + '\n' )
        f.write( 'uNumHidden ' + str(self.numHidden) + '\n' )
        f.write( 'uNumOutput ' + str(self.numOutput) + '\n\n' )
        for i in range(0,self.numHidden):
            f.write( str( self.hidBias[i] ) + '\n' )
            for j in range(0,self.numInput):
                f.write( str( self.hidIn[j][i] ) + '\n' )
            f.write( '\n' )
        for i in range(0,self.numOutput):
            f.write( str( self.outBias[i] ) + '\n' )
            for j in range(0,self.numHidden):
                f.write( str( self.outHid[j][i] ) + '\n' )
            f.write( '\n' )
        if ( len( woutfile ) > 0 ):
            f.close()
    #--
    # setInput()
    # sets network input values based on sensor argument
    #--
    def setInput( self, sensors ):
        for i in range(0,self.numSensors):
            self.x_in[i] = float( sensors[i] / Constants.XMAX ) # scale to value between 0 and 1
    #--
    # getOutput()
    # determines network output, using sensor values as inputs
    #--
    def getOutput( self ):
        # compute values of hidden nodes, by multiplying input values
        # by input-hidden weights and accumulating for each hidden node
        for i in range(0,self.numHidden):
            self.hidSum[i] = self.hidBias[i]
            for j in range(0,self.numInput):
                self.hidSum[i] = self.hidSum[i] + self.hidIn[j][i] * self.x_in[j]
        # apply thresholding function between hidden layer and output layer
        # (This is just how we did it with the original tron neural
        # network players, and since we're using the weights derived
        # from those experiments for this lab exercise, we need to do
        # it consistently here.)
        for i in range(0,self.numHidden):
            self.hid[i] = self.threshold( self.hidSum[i] )
        # compute values of output nodes, by multiplying (squashed)
        # hidden values by hidden-output weights and accumluating for
        # each output node. (Note that normally we would (also) apply
        # the thresholding function at this level. In this case, since
        # we're using the output to indicate which of three activation
        # levels is highest, we don't need to bother with the
        # threshold function---we can save that computation, because
        # we'd still end up with the same relationship between the
        # three outputs (i.e., which is largest), regardless of
        # whether we squashed the output or not.)
        for i in range(0,self.numOutput):
            self.out[i] = self.outBias[i];
            for j in range(0,self.numHidden):
                self.out[i] = self.out[i] + self.outHid[j][i] * self.hid[j]
    #--
    # whereDoIGo()
    # return direction that agent should, given its current location (x,y)
    #--
    def whereDoIGo( self, x, y, arena ):
        if ( self.skipCount < Constants.SKIP_STEPS ):
            self.skipCount = self.skipCount + 1
        else:
            self.skipCount = 0
            #-evaluate sensors
            self.updateSensors( x, y, arena )
            #-set network input
            self.setInput( self.sensors )
            #-determine network output
            self.getOutput()
            #-determine new direction of travel, by translating
            #-network output to agent move based on highest activation
            #-level (left, right, or straight)
            if ( self.out[1] > self.out[0] ):
                if ( self.out[2] > self.out[1] ):
                    self.move = Constants.MOVE_LEFT_TURN
                else:
                    self.move = Constants.MOVE_STRAIGHT
            else:
                if ( self.out[2] > self.out[0] ):
                    self.move = Constants.MOVE_LEFT_TURN
                else:
                    self.move = Constants.MOVE_RIGHT_TURN
            #-wala! we have our new move!
            self.direction = ( self.direction + self.move + 4 ) % 4
            #-record sensor values and new move in log file
            self.logfile.write( str( self ) + '\n' )
        return( self.direction )
    #--
    # threshold()
    # our own version of the tanh function for thresholding the output
    # of the neural network.
    #--
    def threshold( self, s ):
        if ( s < 0 ):
            u = math.exp( 2.0 * s )
            return ((u - 1)/(u + 1))
        else:
            u = math.exp( -2.0 * s )
            return ((1 - u)/(1 + u))
    #--
    # computeError()
    # computes and returns output error, based on target input
    # argument (difference between network output and target output)
    #--
    def computeError( self, target ):
        err = 0.0
        self.d_out = [0.0 for i in range(0,self.numOutput)]
        for i in range(0,self.numOutput):
            self.d_out[i] = target[i] - self.out[i]
            err = err + math.pow( self.d_out[i], 2 )
        err = math.sqrt( err )
        return( err )
    #--
    # initAccumError()
    # initialises an array for storing accumulated error, for batch
    # learning.
    #--
    def initAccumError( self ):
        self.accum_out = [0.0 for i in range(0,self.numOutput)]
        self.num_accum = 0
    #--
    # accumulateError()
    # computes accumulated error, for batch learning. this is the
    # average error over all the training examples that have been seen
    # (stored in self.num_accum). 
    #--
    def accumulateError( self, target ):
        err = self.computeError( target )
        for i in range(0,self.numOutput):
            self.accum_out[i] = self.accum_out[i] + self.d_out[i]
        self.num_accum = self.num_accum + 1
    #--
    # computeAccumError()
    # computes and returns accumulated output error, for batch
    # learning.
    #--
    def computeAccumError( self ):
        err = 0.0
        self.d_out = [0.0 for i in range(0,self.numOutput)]
        for i in range(0,self.numOutput):
            self.d_out[i] = self.accum_out[i] / self.num_accum
            err = err + math.pow( self.d_out[i], 2 )
        err = math.sqrt( err )
        return( err )
    #--
    # train()
    # trains the network weights using backpropagation.
    # ====== these lines have to be rewrite ===== TODO
    # if "batch" learning mode is being used, then adjust weights
    # according to accumulated error, rather than error for current
    # target (which is what is done for "online" mode).
    # ====== these lines have to be rewrite ===== TODO
    #--
    def train( self, target, training ):
        #-initialize partial errors
        d_outBias  = [0.0 for i in range(0,self.numOutput)]
        d_outHid   = [[0.0 for j in range(0,self.numOutput)] for i in range(0,self.numHidden)]
        d_hid      = [0.0 for i in range(0,self.numHidden)]
        d_hidBias  = [0.0 for i in range(0,self.numHidden)]
        d_hidIn    = [[0.0 for j in range(0,self.numHidden)] for i in range(0,self.numInput)]
        #-compute difference between network output and target output
        # TODO
        train_action = {
            Constants.TRAIN_TYPE['BATCH']: self.computeAccumError,
            Constants.TRAIN_TYPE['ONLINE']: partial(self.computeError, target),
            Constants.TRAIN_TYPE['OFFLINE']: partial(self.computeError, target)
        }
        err = train_action[training]()
        
        #-run backpropagation
        for i in range(0,self.numOutput):
            d_outBias[i] = self.momentum * d_outBias[i] + self.d_out[i]
            self.outBias[i] = self.outBias[i] + self.learningRate * d_outBias[i]
            for j in range(0,self.numHidden):
                d_outHid[j][i] = d_outHid[j][i] + self.momentum * d_outHid[j][i] + self.d_out[i] * self.hid[j]
                self.outHid[j][i] = self.outHid[j][i] + self.learningRate * d_outHid[j][i]
                d_hid[j] = d_hid[j] + self.d_out[i] * self.outHid[j][i] * ( 1.0 - self.hid[j] * self.hid[j] )
        for i in range(0,self.numHidden):
            d_hidBias[i] = self.momentum * d_hidBias[i] + d_hid[i]
            d_hidBias[i] = d_hidBias[i] + self.learningRate * d_hidBias[i]
            for j in range(0,self.numInput):
                d_hidIn[j][i] = self.momentum * d_hidIn[j][i] + d_hid[i] * self.x_in[j]
                self.hidIn[j][i] = self.hidIn[j][i] + self.learningRate * d_hidIn[j][i]
        #-return value of error (as it was before adjusting the weights, above)
        return( err )
