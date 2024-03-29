# where should copyover information be stored
LIB_FOLDER            = 'lib/'
DATABASE_FILE         = 'data.db'
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
STARTING_ROOM         = 'stockville[recall]'
VOID_ROOM             = 'stockville[void]'
PLAYER_PROMPT         = '> '

# player preferences
DEFAULT_SCREEN_LENGTH = 50
DEFAULT_SCREEN_WIDTH  = 80
DEFAULT_COLOR_MODE    = '256color'
DEFAULT_BRIEF_MODE    = 0
DEFAULT_ACTIVE_IDLE   = 0
DEFAULT_DEBUG_MODE    = 0

# string maximums
MAX_PLAYER_NAME_LENGTH       = 16  # length of 'responsibilities'

MAX_ZONE_ID_LENGTH           = 12  # length of 'spider_caves'
MAX_ZONE_NAME_LENGTH         = 48

MAX_ROOM_ID_LENGTH           = 12  # length of 
MAX_ROOM_NAME_LENGTH         = 48  # length of 

MAX_OBJECT_ID_LENGTH         = 16  # length of
MAX_OBJECT_NAME_LENGTH       = 46  # length of 

MAX_NPC_ID_LENGTH            = 16  # length of
MAX_NPC_NAME_LENGTH          = 46  # length of 

# player fields
DEFAULT_TITLE         = "the title-less"

# starting rooms
VOID_ROOM             = "stockville[void]"