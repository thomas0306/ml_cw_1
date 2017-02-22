class Constants( object ):
    #-define compasss directions for player movement
    SOUTH = 0
    EAST  = 1
    NORTH = 2
    WEST  = 3
    #-define bounds for the arena
    XMIN = 0
    XMAX = 256
    YMIN = 0
    YMAX = 256
    #-define number of pixels between moves for agent players
    SKIP_STEPS = 3
    #-define moves
    MOVE_RIGHT_TURN = -1
    MOVE_STRAIGHT   =  0
    MOVE_LEFT_TURN  =  1
    MOVE_NAMES = ( 'RIGHT', 'STRAIGHT', 'LEFT' )

    #-define train type
    # TODO
    TRAIN_TYPE = {
        'BATCH': 'BATCH',
        'ONLINE': 'ONLINE',
        'OFFLINE': 'OFFLINE'
    }

    # PATH
    DATA_ROOT = 'data/'

    RAW_DATA_PATH = '%sraw_data/' % DATA_ROOT
    PROCESSED_DATA_PATH = '%sprocessed_data/' % DATA_ROOT
    TRAIN_LOG_PATH = '%strain_log/' % DATA_ROOT
    TRAINED_NN_PATH = '%strained_nn/' % DATA_ROOT
    PLOT_PATH = '%splot/' % DATA_ROOT


