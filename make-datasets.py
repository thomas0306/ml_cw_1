#--
# make-datasets.py
# 18-feb-2017/sklar
# This program makes three balanced data sets for training, validation
# and evaluation of a machine learner (the learning isn't done in
# program, only the balancing of the raw data set and the dividing of
# it into three subsets.
#--

import sys
import re
import random


#-check if the number of command-line arguments meets the minimum for
# this command format.
if ( len( sys.argv ) < 2 ):
    print 'usage error: ' + sys.argv[0] + ' <input-file-name>'
    sys.exit()
#-get input filename, which should be first command-line argument
input_filename = sys.argv[1]
#-initialise names for training, validation and evaluation data sets
train_filename = 'train-' + input_filename
valid_filename = 'valid-' + input_filename
eval_filename  = 'eval-'  + input_filename

#-read contents of input file into a list called "rawdata"
try:
    f = open( input_filename, 'r' )
    rawdata = f.readlines()
    f.close()
except IOError as iox:
    print 'error opening file [' + filename + ']: ' + str( iox )
    sys.exit()
#-save the number of records in the list
numrec = len( rawdata )

#-sort into left, right and straight moves
L = []
R = []
S = []
#-loop through all the records in the raw data list
for rec in rawdata:
    # split each record into its constituent fields
    fields = re.split( '[ \t]', rec.strip() )
    # save the robot's "move"
    move = fields[12]
    # based on which move was made, store the whole record (which also
    # includes the sensor readings) in the list corresponding to that
    # move
    if ( move == 'LEFT' ):
        L.append( rec.strip() )
    elif ( move == 'RIGHT' ):
        R.append( rec.strip() )
    elif ( move == 'STRAIGHT' ):
        S.append( rec.strip() )

#-done with looping through raw data. now save and report the number
# of records in each move-specific list.
numL = len( L )
numR = len( R )
numS = len( S )
print 'number of records   = {0:4d}'.format( numrec )
print 'number of LEFTs     = {0:4d} ({1:4.2f}%)'.format( numL, 1.0*numL/numrec )
print 'number of RIGHTs    = {0:4d} ({1:4.2f}%)'.format( numR, 1.0*numR/numrec )
print 'number of STRAIGHTs = {0:4d} ({1:4.2f}%)'.format( numS, 1.0*numS/numrec )

#-now we're ready to create a balanced data set.
#
#-there are two ways to make a balanced data set:
# (1) repeat the under-represented records enough times to be equal to
# the number of over-represented records; or
# (2) delete enough of the over-represented records so that the number
# left are equal to the number of under-represented records.
# because we don't have a lot of data to begin with, we'll try the
# first way.
#
#-first let's determine computationally how many records we want of
# each type by finding the largest of the three counts and setting
# "maxnum" to that value.
maxnum = max( numL, numR, numS )

#-then we loop through the records for each type, adding copies of
# randomly selected records as we need to in order to bring the count
# up to maxnum.
#-initialise balanced data set with full set of original records
balanced_S = list( S ) 
#-then enough more randomly selected copies of records to meet maxnum
while( len(balanced_S) < maxnum ):
    i = random.randint( 0, len(S)-1 )
    balanced_S.append( S[i] )
#-do the same thing for the RIGHTs
balanced_R = list( R )
while( len(balanced_R) < maxnum ):
    i = random.randint( 0, len(R)-1 )
    balanced_R.append( R[i] )
#-and the LEFTs
balanced_L = list( L )
while( len(balanced_L) < maxnum ):
    i = random.randint( 0, len(L)-1 )
    balanced_L.append( L[i] )

#-now we have a balanced master data set.
#-so let's split that into three pieces: training, validation and evaluation.
#-first we open the three output data files
try:
    ft = open( train_filename, 'w' )
    fv = open( valid_filename, 'w' )
    fe = open( eval_filename, 'w' )
except IOError as iox:
    print 'error opening file: ' + str( iox )
    sys.exit()
#-then we "deal" records into each file...
j = 0
for i in range( 0, maxnum ):
    if ( j == 0 ):
        ft.write( balanced_L[i] + '\n' )
        ft.write( balanced_R[i] + '\n' )
        ft.write( balanced_S[i] + '\n' )
        j = 1
    elif ( j == 1 ):
        fv.write( balanced_L[i] + '\n' )
        fv.write( balanced_R[i] + '\n' )
        fv.write( balanced_S[i] + '\n' )
        j = 2
    elif ( j == 2 ):
        fe.write( balanced_L[i] + '\n' )
        fe.write( balanced_R[i] + '\n' )
        fe.write( balanced_S[i] + '\n' )
        j = 0
#-close up the files before we go home
ft.close()
fv.close()
fe.close()

#-and that's all folks!!

