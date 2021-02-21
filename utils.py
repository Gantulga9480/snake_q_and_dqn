import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 177, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

WIDTH = 540
HEIGHT = 600
VELOCITY = 50
SHAPE = VELOCITY - 1
FPS = 60
BOARD_COUNT = int((WIDTH - 40) / VELOCITY)

HEAD = 66
TAIL = 33
FOOD = 99
EMPTY = 0

#                ↑, →, ↓, ←
STATE_SPACE = {'[0, 0, 0, 33]': 0,
               '[0, 0, 33, 0]': 1,
               '[0, 0, 33, 33]': 2,
               '[0, 33, 0, 0]': 3,
               '[0, 33, 0, 33]': 4,
               '[0, 33, 33, 0]': 5,
               '[0, 33, 33, 33]': 6,
               '[33, 0, 0, 0]': 7,
               '[33, 0, 0, 33]': 8,
               '[33, 0, 33, 0]': 9,
               '[33, 0, 33, 33]': 10,
               '[33, 33, 0, 0]': 11,
               '[33, 33, 0, 33]': 12,
               '[33, 33, 33, 0]': 13,
               '[33, 33, 33, 33]': 14,
               '[0, 0, 33, 99]': 15,
               '[0, 33, 0, 99]': 16,
               '[0, 33, 33, 99]': 17,
               '[33, 0, 0, 99]': 18,
               '[33, 0, 33, 99]': 19,
               '[33, 33, 0, 99]': 20,
               '[33, 33, 33, 99]': 21,
               '[0, 0, 99, 33]': 22,
               '[0, 33, 99, 0]': 23,
               '[0, 33, 99, 33]': 24,
               '[33, 0, 99, 0]': 25,
               '[33, 0, 99, 33]': 26,
               '[33, 33, 99, 0]': 27,
               '[33, 33, 99, 33]': 28,
               '[0, 99, 0, 33]': 29,
               '[0, 99, 33, 0]': 30,
               '[0, 99, 33, 33]': 31,
               '[33, 99, 0, 0]': 32,
               '[33, 99, 0, 33]': 33,
               '[33, 99, 33, 0]': 34,
               '[33, 99, 33, 33]': 35,
               '[99, 0, 0, 33]': 36,
               '[99, 0, 33, 0]': 37,
               '[99, 0, 33, 33]': 38,
               '[99, 33, 0, 0]': 39,
               '[99, 33, 0, 33]': 40,
               '[99, 33, 33, 0]': 41,
               '[99, 33, 33, 33]': 42}

# 0: forward, 1: left, 2: right
ACTION_SPACE = [0, 1, 2, 3]
FOOD_REWARD = math.sqrt(BOARD_COUNT**2 + BOARD_COUNT**2)
OUT_REWARD = - FOOD_REWARD * BOARD_COUNT
EMPTY_STEP_REWARD = -2

WINDOW_SIZE = 3


def pad_with(vector, pad_width, _, kwargs):
    pad_value = kwargs.get('padder', TAIL)
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value
