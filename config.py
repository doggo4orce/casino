# where should copyover information be stored
LIB_FOLDER            = 'lib/'
COPYOVER_FILE         = 'copyover.dat'
COPYOVER_PATH         = LIB_FOLDER + COPYOVER_FILE

# where the world files are stored
WORLD_FOLDER          = LIB_FOLDER + 'world/'
WLD_FOLDER            = WORLD_FOLDER + 'wld/'
NPC_FOLDER            = WORLD_FOLDER + 'npc/'
OBJ_FOLDER            = WORLD_FOLDER + 'obj/'
ZON_FOLDER            = WORLD_FOLDER + 'zon/'
	
# where player index should be stored
PFILES_FOLDER         = 'pfiles/'
PLAYER_INDEX_FILE     = 'index'
PFILES_PATH           = LIB_FOLDER + PFILES_FOLDER
PLAYER_INDEX_PATH     = PFILES_PATH + PLAYER_INDEX_FILE

# configurable administrative constants
MAX_INPUT_LENGTH      = 512
MIN_PASSWORD_LENGTH   = 3
MAX_PASSWORD_LENGTH   = 20
PACKET_SIZE           = 256 # max bytes to read from socket each poll
OMUD_VERSION          = '1.0 alpha'

# configurable gameplay constants
STARTING_ROOM         = 'casino[temple]'
VOID_ROOM             = 'casino[temple]'
PLAYER_PROMPT         = '> '

# player preferences
DEFAULT_SCREEN_LENGTH = 50
DEFAULT_SCREEN_WIDTH  = 80
DEFAULT_COLOR_MODE    = '256'
DEFAULT_BRIEF_MODE    = 'off'
DEFAULT_ACTIVE_IDLE   = 'off'
DEFAULT_DEBUG_MODE    = 'off'

# player fields
DEFAULT_TITLE         = "the title-less"