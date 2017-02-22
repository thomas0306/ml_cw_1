#--
# train-online.py
# This program is extended from Dr. Sklar's train-batch.py
#
# Kwan Hau Thomas, LEE
# 1650501
#
# This program demonstrates the idea of "offline" training for a neural
# network.
#
# The offline training mode adjust weights based on the error of each
# instance in the training set. It seen and adjusted one at a time. But
# the learner will go through the whole training set more than one times.
#
# This code also uses a "validation" data set, as well as a training
# data set, to report on the progress of the learner based on data
# that it is not using to adjust its weights.
#
# This program can be run from the command-line as:
#  $ python train-offline.py train.dat valid.dat eval.dat weights.dat training.log
# where: 
#  train.dat    = training data set (input)
#  valid.dat    = validation data set (input)
#  eval.dat     = evaluation data set (input)
#  weights.dat  = learned weights (output)
#  training.log = training log (output)
#
#--

import sys
import re
from nn import NNPlayer
import os
import time
from const import Constants
from matplotlib import pyplot as plt
import numpy as np

MAX_TRAINING_STEPS = 1


#--
# readDataset()
# this function reads the contents of a data file into a list called
# "dataset", which the function returns.
#--
def readDataset( filename ):
    try:
        f = open( filename, 'r' )
        dataset = f.readlines()
        f.close()
    except IOError as iox:
        print 'error opening data file (' + filename + '): ' + str(  iox )
        sys.exit()
    return( dataset )


#--
# evaluate()
# this function evaluates the player "p" against the data set found in
# the argument "datafile".
# the function returns the average error over the number of records in
# the evaluation data set.
#--
def evaluate( p, eval_data ):
    sensors = [0 for i in range(0,8)]
    total_error = 0
    recnum = 0
    for rec in eval_data:
        fields = re.split( '[ \t]', rec.strip() )
        for i in range(0,8):
            sensors[i] = float( fields[i+3] )
        move = fields[12]
        if ( move == 'RIGHT' ):
            target = [ 1, 0, 0 ]
        elif ( move == 'LEFT' ):
            target = [ 0, 0, 1 ]
        else:
            target = [ 0, 1, 0 ]
        p.setInput( sensors )
        p.getOutput()
        total_error = total_error + p.computeError( target )
        recnum = recnum + 1
    return( total_error / recnum )



########## MAIN PROGRAM ##########

#-check if the number of command-line arguments meets the minimum for
# this command format.
if ( len( sys.argv ) < 5 ):
    print 'usage error: ' + sys.argv[0] + ' <training-data> <validation-data> <evaluation-data> <weights> <log>'
    sys.exit()
#-get command-line arguments
training_data_filename   = Constants.PROCESSED_DATA_PATH + sys.argv[1]
validation_data_filename = Constants.PROCESSED_DATA_PATH + sys.argv[2]
evaluation_data_filename = Constants.PROCESSED_DATA_PATH + sys.argv[3]
output_weights_filename  = Constants.TRAINED_NN_PATH + sys.argv[4]
log_filename             = Constants.TRAIN_LOG_PATH + sys.argv[5]

#-read contents of training data file into a list called "train_data".
train_data = readDataset( training_data_filename )
# save the number of records in the training data
numrec = len( train_data )
print 'training data file = ' + training_data_filename + ' number of records = ' + str( numrec )

#-read contents of validation data file into a list called "val_data".
val_data = readDataset( validation_data_filename )
print 'validation data file = ' + validation_data_filename + ' number of records = ' + str( len( val_data ))

#-read contents of evaluation data file into a list called "eval_data".
eval_data = readDataset( evaluation_data_filename )
print 'evaluation data file = ' + evaluation_data_filename + ' number of records = ' + str( len( eval_data ))

#-instantiate an NNPlayer object, with random weights
p = NNPlayer( 1, '', '' )

#-initialise a list of 8 sensors
sensors = [0 for i in range(0,8)]

#-open log file for recording how error rate changes.
try:
    f = open( log_filename, 'w' )
except IOError as iox:
    print 'error opening log file: ' + str( iox )
    sys.exit()

#-loop through the raw data
gen = 0
recnum = 0
# init error
train_error = float('inf')
train_error_history = []
val_error_history = np.array([])
e = 0.001
keep_train = True

while keep_train:
# for i in range(0,MAX_TRAINING_STEPS):
    # loop through all examples
    
    for trec in train_data:
        fields = re.split( '[ \t]', trec.strip() )
        for i in range(0,8):
            sensors[i] = float( fields[i+3] )
        move = fields[12]
        if ( move == 'RIGHT' ):
            target = [ 1, 0, 0 ]
        elif ( move == 'LEFT' ):
            target = [ 0, 0, 1 ]
        else:
            target = [ 0, 1, 0 ]
        p.setInput( sensors )
        p.getOutput()
        recnum = recnum + 1
        # update weights for each examples
        train_error = p.train( target, Constants.TRAIN_TYPE['OFFLINE'] )
        train_error_history.append(train_error)
    gen = gen + 1
    print 'record ' + str( recnum ),
    print ' generation ' + str( gen ),
    print ' training_error ' + str( train_error ),
    f.write( 'record ' + str( recnum ))
    f.write( ' generation ' + str( gen )) 
    f.write( ' training_error ' + str( train_error ))
    # if ( gen % 100 == 0 ):
        # every 100 generations, evaluate against the validation data set
    val_error = evaluate( p, val_data )
    if len(val_error_history) and (val_error > val_error_history[-1] or abs(val_error - val_error_history[-1]) <= e):
        keep_train = False
    if len(val_error_history):
        val_error_history = np.append(val_error_history, np.arange(val_error_history[-1], val_error, -abs(val_error-val_error_history[-1])/len(train_data)))
    else:
        val_error_history = np.array([val_error])
    f.write( ' validation_error ' + str( val_error ))
    print ' validation_error ' + str( val_error ),
    f.write( '\n' )
    print
# done training
val_error = evaluate( p, val_data )
print 'record ' + str( recnum ),
print ' generation ' + str( gen ),
print ' training_error ' + str( train_error ),
print ' validation_error ' + str( val_error )

# plot error rate
plt.figure()
plt.plot(train_error_history)
plt.plot(val_error_history)
plt.title('Error Rate Plot')
plt.ylabel('error rate')
plt.xlabel('epochs')
if not os.path.exists('plot'):
    os.makedirs('plot')
plt.savefig('%serror_plot_%d.png' % (Constants.PLOT_PATH, int(time.time())))

#-save nn weights
p.printNetwork( output_weights_filename )

#-evaluate against evaluation data set
eval_error = evaluate( p, eval_data )
print 'evaluation error ' + str( eval_error )
f.write( ' evaluation_error ' + str( eval_error ) + '\n')

#-close log file
f.close()

#-and that's all folks!!