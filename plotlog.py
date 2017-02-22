#--
# plotlog.py
# 10-feb-2017/sklar
#
# This program generates a plot of the error from the training log.
# log file format:
#  column 0: "record"
#  column 1: training record number (record in file of training set data)
#  column 2: "generation"
#  column 3: training generation number
#  column 4: "training_error"
#  column 5: error rate (the data we want to plot)
#  column 6: "validation_error" (only every 100 generations)
#  column 7: validation error (only every 100 generations)
#
# This program can be run from the command-line as:
#  $ python plotlog.py training.log plotfile.png
# where: 
#  training.log = training log (input)
#  plotfile.png = plot of training and validation errors, over time (output)
#
#--

import sys
import re
import matplotlib.pyplot as plt

#-check if the number of command-line arguments meets the minimum for
# this command format.
if ( len( sys.argv ) < 3 ):
    print 'usage error: ' + sys.argv[0] + ' <log-file-name> <plot-file-name>'
    sys.exit()
#-get command-line arguments
log_filename = sys.argv[1]
plot_filename = sys.argv[2]

#-read contents of log file into a list called "rawdata".
try:
    f = open( log_filename, 'r' )
    rawdata = f.readlines()
    f.close()
except IOError as iox:
    print 'error opening log file: ' + str( iox )
    sys.exit()

#-loop through the raw data and save the error rates in a list.
train_gen = []
train_error = []
val_gen = []
val_error = []
for rec in rawdata:
    fields = re.split( '[ \t]', rec.strip() )
    train_gen.append( int( fields[3] ))
    train_error.append( float( fields[5] ))
    if ( len( fields ) > 6 ):
        val_gen.append( int( fields[3] ))
        val_error.append( float( fields[7] ))

#-plot data
plt.figure()
te = plt.plot( train_gen, train_error, 'b', label='training error' )
plt.hold( True )
ve = plt.plot( val_gen, val_error, 'r', label='validation error' )
plt.legend()
#plt.ylim(( 0, 3 ))
plt.savefig( plot_filename )
plt.show()

#-and that's all folks!!
