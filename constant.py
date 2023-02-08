
TITLE = "てくてく沙花叉"
SCREEN_SCALE = 50
SCREEN_HEIGHT = int(10*SCREEN_SCALE) #ゲーム画面縦幅
SCREEN_WIDTH = int(16*SCREEN_SCALE) #ゲーム画面横幅
SCREEN_CENTER = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)

START_SCREEN_COLOR = (230,100,80)
START_SCREEN_WIDTH = SCREEN_WIDTH//2
START_SCREEN_HEIGHT = SCREEN_HEIGHT//3
START_BUTTON_WIDTH = START_SCREEN_WIDTH//2
START_BUTTON_HEIGHT = START_SCREEN_HEIGHT//3

TEXT_SIZE_VERY_SMALL = SCREEN_HEIGHT//20
TEXT_SIZE_SMALL = SCREEN_HEIGHT//15
TEXT_SIZE_MIDDLE = SCREEN_HEIGHT//10
TEXT_SIZE_LARGE = SCREEN_HEIGHT//5
TEXT_COLOR_RED = (230,100,80)
TEXT_COLOR_WHITE = (255,255,255)
TEXT_BG_DEFAULT_COLOR = (255,255,255)

#JUMP_BUTTON_RECT_CENTER = ((SCREEN_WIDTH*5)//6,(SCREEN_HEIGHT*3)//4)
#JUMP_BUTTON_WIDTH = SCREEN_WIDTH//6
#JUMP_BUTTON_HEIGHT = SCREEN_HEIGHT//5

RESULTS_SCREEN_COLOR = (230,100,80)

UI_COLOR = (230,100,80)
UI_HEIGHT = SCREEN_HEIGHT//8
HP_GAUGE_WIDTH = SCREEN_WIDTH//2
HP_GAUGE_HEIGHT = int(UI_HEIGHT*0.8)
DISTANCE_DISPLAY_WIDTH = SCREEN_WIDTH//2
DISTANCE_DISPLAY_HEIGHT = UI_HEIGHT

FIELD_BLOCK_WIDTH = SCREEN_WIDTH//3
NUM_OF_OBSTRUCTION_PER_FIELDUNIT = 3

GRAVITY = 0.5
FPS = 60

CHARA_NAME = "Chloe"
PLAYER_SCALE = 0.15
CHARA_INIT_POS = (-30,350)
PLAYER_HP = 3
CHARA_DEFAULT_POS = (60,350)
ENEMY_SCALE = 0.2
ENEMY_HP = 1
ENEMY_VELOSITY_X = -1#-2.5
NUM_OF_ENEMY_TYPE = 2
BG_SCALE = 1
NEAR_BG_VELOSITY_X = -1.2

BG_SKY_COLOR = (110,170,250) #水色
BG_FLOOR_COLOR = (140,140,140)#灰色 #(200,100,50) 茶色
BG_FLOOR_HEIGHT = SCREEN_HEIGHT//8
GROUND_POSITION = (0,SCREEN_HEIGHT-BG_FLOOR_HEIGHT)

ANIMATION_COOLDOWN = 250
DISTANCE_ANIMATION_COOLDOWN = ANIMATION_COOLDOWN//2

BG_UNIT_IMG_PATH = "img/background/"
UI_IMG_PATH = "img/ui/"
ANIMATION_IMG_PATH = "img/chara/"
OBSTRUCTION_IMG_PATH = 'img/obstruction/'

