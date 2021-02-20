import pygame
import numpy as np
import math as mt
from utils import *


def init():
    pygame.init()
    pygame.display.set_caption("SNAKE")


class Snake:

    def __init__(self):
        self.fps = FPS
        self.vel = VELOCITY
        self.shape = SHAPE
        self.font = pygame.font.SysFont("arial", 25)
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.board = np.zeros((BOARD_COUNT, BOARD_COUNT), dtype=int)
        self.snake = list()
        self.food_x = 0
        self.food_y = 0
        self.head = False
        self.out = False
        self.over = False
        self.food_hit = False
        self.game_flip = True
        self.run = True
        self.score = 0
        self.ldir = ""

        self.dis_diff = 0

    def step(self, action=None):
        self.over = False
        if self.game_flip:
            self.draw_game()
        tmp = self.snake[0][2]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.over = True
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_flip:
                        self.game_flip = True
                    elif self.game_flip:
                        self.game_flip = False
                elif event.key == pygame.K_UP:
                    self.fps += 2
                elif event.key == pygame.K_DOWN:
                    self.fps -= 2
        self.get_action(action)
        for index, block in enumerate(self.snake):
            if index == 0:
                self.head = True
                if self.snake[0][0] == self.food_x and \
                        self.snake[0][1] == self.food_y:
                    self.board[self.food_y][self.food_x] = HEAD
                    self.food_hit = True
                    do = True
                    while do:
                        self.food_x = np.random.randint(0, BOARD_COUNT - 1)
                        self.food_y = np.random.randint(0, BOARD_COUNT - 1)
                        if self.board[self.food_y][self.food_x] == TAIL:
                            pass
                        else:
                            do = False
                    self.board[self.food_y][self.food_x] = FOOD
                    tail = self.snake[len(self.snake) - 1].copy()
                    if tail[2] == "↑":
                        tail[1] += 1
                    elif tail[2] == "↓":
                        tail[1] -= 1
                    elif tail[2] == "←":
                        tail[0] += 1
                    elif tail[2] == "→":
                        tail[0] -= 1
                    self.snake.append(tail)
            else:
                self.head = False
                tmp = block[2]
                block[2] = self.ldir
            if self.out:
                pass
            else:
                self.snake[index] = self.draw_snake(block.copy())
            self.ldir = tmp
        self.score = len(self.snake) - 3
        return self.feedback()

    def feedback(self):
        if self.out:
            self.over = True
            return self.over, self.three_state(), OUT_REWARD
        elif self.food_hit:
            self.food_hit = False
            self.dis_diff = self.get_dis()
            return self.over, self.three_state(), self.reward_func()
        else:
            return self.over, self.three_state(), self.reward_func()

    def reward_func(self):
        dis = self.get_dis()
        print(dis)
        if dis <= self.dis_diff:
            self.dis_diff = dis
            return FOOD_REWARD - dis
        else:
            self.dis_diff = dis
            return -2

    def get_dis(self):
        y = self.snake[0][0]
        x = self.snake[0][1]
        print(x, y)
        diff_x = self.food_x - x
        diff_y = self.food_y - y
        dis = mt.sqrt((diff_x**2 + diff_y**2))
        return dis

    def get_window(self):
        head_y = self.snake[0][0]
        head_x = self.snake[0][1]
        win_x = head_x - WINDOW_SIZE//2
        win_y = head_y - WINDOW_SIZE//2
        board = np.pad(self.board, WINDOW_SIZE//2, pad_with)
        board = board[win_x+WINDOW_SIZE//2:WINDOW_SIZE,
                      win_y+WINDOW_SIZE//2:WINDOW_SIZE]
        if self.snake[0][2] == "↑":
            return board
        elif self.snake[0][2] == "←":
            return np.rot90(board, 1)
        elif self.snake[0][2] == "↓":
            return np.rot90(board, 2)
        elif self.snake[0][2] == "→":
            return np.rot90(board, 3)

    def three_state(self):
        state = []
        y = self.snake[0][0]
        x = self.snake[0][1]
        state.append(x)
        state.append(y)
        state.append(self.food_x)
        state.append(self.food_y)
        node = []
        if self.snake[0][2] == "↑":
            if 0 <= y - 1:
                node.append(self.board[x][y-1])
            else:
                node.append(TAIL)
            if x - 1 >= 0:
                node.append(self.board[x-1][y])
            else:
                node.append(TAIL)
            if y + 1 < BOARD_COUNT:
                node.append(self.board[x][y+1])
            else:
                node.append(TAIL)
        elif self.snake[0][2] == "→":
            if x - 1 >= 0:
                node.append(self.board[x-1][y])
            else:
                node.append(TAIL)
            if y + 1 < BOARD_COUNT:
                node.append(self.board[x][y+1])
            else:
                node.append(TAIL)
            if x + 1 < BOARD_COUNT:
                node.append(self.board[x+1][y])
            else:
                node.append(TAIL)
        elif self.snake[0][2] == "↓":
            if y + 1 < BOARD_COUNT:
                node.append(self.board[x][y+1])
            else:
                node.append(TAIL)
            if x + 1 < BOARD_COUNT:
                node.append(self.board[x+1][y])
            else:
                node.append(TAIL)
            if 0 <= y - 1:
                node.append(self.board[x][y-1])
            else:
                node.append(TAIL)
        elif self.snake[0][2] == "←":
            if x + 1 < BOARD_COUNT:
                node.append(self.board[x+1][y])
            else:
                node.append(TAIL)
            if 0 <= y - 1:
                node.append(self.board[x][y-1])
            else:
                node.append(TAIL)
            if x - 1 >= 0:
                node.append(self.board[x-1][y])
            else:
                node.append(TAIL)
        state.append(STATE_SPACE[str(node)])
        return np.array(state, dtype=int)

    def get_action(self, action):
        if self.snake[0][2] == "↑":
            if action == 0:
                pass
            elif action == 1:
                self.snake[0][2] = "←"
            elif action == 2:
                self.snake[0][2] = "→"
        elif self.snake[0][2] == "←":
            if action == 0:
                pass
            elif action == 1:
                self.snake[0][2] = "↓"
            elif action == 2:
                self.snake[0][2] = "↑"
        elif self.snake[0][2] == "↓":
            if action == 0:
                pass
            elif action == 1:
                self.snake[0][2] = "→"
            elif action == 2:
                self.snake[0][2] = "←"
        elif self.snake[0][2] == "→":
            if action == 0:
                pass
            elif action == 1:
                self.snake[0][2] = "↑"
            elif action == 2:
                self.snake[0][2] = "↓"
        return self.snake[0][2]

    def reset(self):
        self.out = False
        self.food_hit = False
        self.snake.clear()
        self.board = np.zeros((BOARD_COUNT, BOARD_COUNT), dtype=int)
        self.over = False
        d = np.random.randint(1, 5)
        ldir = ""
        x, y = 0, 0
        rand_food_x, rand_food_y = 0, 0
        if d == 1:
            ldir = "↓"
            rand_x = np.random.randint(0, BOARD_COUNT - 1)
            x = rand_x
            x_1 = x
            x_2 = x
            rand_y = np.random.randint(2, BOARD_COUNT - 2)
            y = rand_y
            y_1 = y - 1
            y_2 = y_1 - 1
            self.board[x][y] = HEAD
            self.board[x_1][y_1] = TAIL
            self.board[x_2][y_2] = TAIL
        elif d == 2:
            ldir = "→"
            rand_y = np.random.randint(0, BOARD_COUNT - 1)
            y = rand_y
            y_1 = y
            y_2 = y
            rand_x = np.random.randint(2, BOARD_COUNT - 2)
            x = rand_x
            x_1 = x - 1
            x_2 = x_1 - 1
            self.board[x][y] = HEAD
            self.board[x_1][y_1] = TAIL
            self.board[x_2][y_2] = TAIL
        elif d == 3:
            ldir = "↑"
            rand_x = np.random.randint(0, BOARD_COUNT - 1)
            x = rand_x
            x_1 = x
            x_2 = x
            rand_y = np.random.randint(1, BOARD_COUNT - 3)
            y = rand_y
            y_1 = y + 1
            y_2 = y_1 + 1
            self.board[x][y] = HEAD
            self.board[x_1][y_1] = TAIL
            self.board[x_2][y_2] = TAIL
        elif d == 4:
            ldir = "←"
            rand_x = np.random.randint(1, BOARD_COUNT - 3)
            x = rand_x
            x_1 = x + 1
            x_2 = x_1 + 1
            rand_y = np.random.randint(0, BOARD_COUNT - 1)
            y = rand_y
            y_1 = y
            y_2 = y
            self.board[x][y] = HEAD
            self.board[x_1][y_1] = TAIL
            self.board[x_2][y_2] = TAIL
        do = True
        while do:
            rand_food_x = np.random.randint(0, BOARD_COUNT - 1)
            rand_food_y = np.random.randint(0, BOARD_COUNT - 1)
            if self.board[rand_food_y][rand_food_x] == TAIL:
                pass
            else:
                do = False
        self.snake.append([x, y, ldir])
        self.snake.append([x_1, y_1, ldir])
        self.snake.append([x_2, y_2, ldir])
        self.board[rand_food_x][rand_food_y] = FOOD
        self.food_x = rand_food_x
        self.food_y = rand_food_y
        self.dis_diff = self.get_dis()
        return self.three_state()

    def draw_snake(self, block_s):
        y = block_s[0]
        x = block_s[1]
        try:
            if block_s[2] == "↑":
                if y == 0 or self.board[y-1][x] == TAIL:
                    self.out = True
                else:
                    if self.head:
                        self.board[y-1][x] = HEAD
                    else:
                        self.board[y-1][x] = TAIL
                    self.board[y][x] = 0
                    block_s[1] -= 1
            elif block_s[2] == "↓":
                if y == BOARD_COUNT - 1 or self.board[y+1][x] == TAIL:
                    self.out = True
                else:
                    if self.head:
                        self.board[y+1][x] = HEAD
                    else:
                        self.board[y+1][x] = TAIL
                    self.board[y][x] = 0
                    block_s[1] += 1
            elif block_s[2] == "←":
                if x == 0 or self.board[y][x-1] == TAIL:
                    self.out = True
                else:
                    if self.head:
                        self.board[y][x-1] = HEAD
                    else:
                        self.board[y][x-1] = TAIL
                    self.board[y][x] = 0
                    block_s[0] -= 1
            elif block_s[2] == "→":
                if x == BOARD_COUNT - 1 or self.board[y][x+1] == TAIL:
                    self.out = True
                else:
                    if self.head:
                        self.board[y][x+1] = HEAD
                    else:
                        self.board[y][x+1] = TAIL
                    self.board[y][x] = 0
                    block_s[0] += 1
            return block_s.copy()
        except IndexError:
            print(self.head)
            print(x, y, block_s[2])
            print(self.board)
            quit()

    def draw_game(self):
        self.win.fill((0, 0, 0))
        pygame.draw.line(self.win, WHITE,
                         (20, 20),
                         (20, 520))
        pygame.draw.line(self.win, WHITE,
                         (20 + BOARD_COUNT * VELOCITY, 20),
                         (20 + BOARD_COUNT * VELOCITY, 520))
        pygame.draw.line(self.win, WHITE,
                         (20, 20),
                         (520, 20))
        pygame.draw.line(self.win, WHITE,
                         (20, 20 + BOARD_COUNT * VELOCITY),
                         (520, 20 + BOARD_COUNT * VELOCITY))
        score = self.font.render(f"Score: {self.score}", 1, WHITE)
        self.win.blit(score, (200, 540))
        food_drawn = False
        for i in range(BOARD_COUNT):
            for j in range(BOARD_COUNT):
                if self.board[i][j] == HEAD:
                    pygame.draw.rect(self.win, YELLOW,
                                     (self.vel*j+21, self.vel*i+21,
                                      self.shape, self.shape))
                elif self.board[i][j] == TAIL:
                    pygame.draw.rect(self.win, RED,
                                     (self.vel*j+21, self.vel*i+21,
                                      self.shape, self.shape))
                elif self.board[i][j] == FOOD:
                    food_drawn = True
                    pygame.draw.rect(self.win, GREEN,
                                     (self.vel*j+21, self.vel*i+21,
                                      self.shape, self.shape))
        pygame.display.flip()
        self.clock.tick(self.fps)
        if not food_drawn:
            do = True
            while do:
                rand_food_x = np.random.randint(0, BOARD_COUNT - 1)
                rand_food_y = np.random.randint(0, BOARD_COUNT - 1)
                if self.board[rand_food_y][rand_food_x] == TAIL:
                    pass
                else:
                    do = False
            self.board[rand_food_y][rand_food_x] = FOOD
            self.food_x = rand_food_x
            self.food_y = rand_food_y
            pass
