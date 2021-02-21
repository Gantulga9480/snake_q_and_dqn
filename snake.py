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
        self.game_flip = True
        self.run = True
        self.debug = False

        self.board = np.zeros((BOARD_COUNT, BOARD_COUNT), dtype=int)
        self.snake = list()
        self.food_x = 0
        self.food_y = 0
        self.dis_diff = 0
        self.out = False
        self.over = False
        self.food_hit = False
        self.win_state = {}
        self.win_state_counter = 0

    def step(self, action=None):
        # self.check_snake()
        if self.game_flip:
            self.draw_game(self.board)
        self.handle_event()
        for i, block in reversed(list(enumerate(self.snake))):
            if i == 0:
                self.get_action_dir(action)
            else:
                block[2] = self.snake[i-1][2]
            self.snake[i] = self.draw_snake(block, i)
        self.food_check()
        return self.feedback()

    def feedback(self):
        if self.out:
            self.over = True
            return self.over, self.get_state(), OUT_REWARD
        elif self.food_hit:
            self.food_hit = False
            # self.dis_diff = self.get_dis()
            return self.over, self.get_state(), FOOD_REWARD
        else:
            return self.over, self.get_state(), self.reward_func()

    def get_state(self):
        return self.four_state()
        return self.get_window()

    def reward_func(self):
        # dis = self.get_dis()
        # self.dis_diff = dis
        # if dis <= self.dis_diff:
        #     return EMPTY_STEP_REWARD*5
        # else:
        return EMPTY_STEP_REWARD*5

    def get_dis(self):
        diff_x = self.food_x - self.snake[0][0]
        diff_y = self.food_y - self.snake[0][1]
        dis = mt.sqrt((diff_x**2 + diff_y**2))
        return dis

    def get_window(self):
        state = []
        x = self.snake[0][0]
        y = self.snake[0][1]
        dis_x = self.food_x - x
        dis_y = self.food_y - y
        if dis_x < 0 and dis_y < 0:
            state.append(0)
        elif dis_x < 0 and dis_y == 0:
            state.append(1)
        elif dis_x < 0 and dis_y > 0:
            state.append(2)
        elif dis_x == 0 and dis_y > 0:
            state.append(3)
        elif dis_x > 0 and dis_y > 0:
            state.append(4)
        elif dis_x > 0 and dis_y == 0:
            state.append(5)
        elif dis_x > 0 and dis_y < 0:
            state.append(6)
        elif dis_x == 0 and dis_y < 0:
            state.append(7)
        elif dis_x == 0 and dis_y == 0:
            quit()
        win_x = self.snake[0][0]
        win_y = self.snake[0][1]
        end_x = win_x + WINDOW_SIZE
        end_y = win_y + WINDOW_SIZE
        board = np.pad(self.board, WINDOW_SIZE//2)
        board = board[win_x:end_x, win_y:end_y]
        nodes = str(board.flatten())
        if nodes not in self.win_state:
            self.win_state[nodes] = self.win_state_counter
            self.win_state_counter += 1
        state.append(self.win_state[nodes])
        return str(state)

    def four_state(self):
        state = []
        x = self.snake[0][0]
        y = self.snake[0][1]
        dis_x = self.food_x - x
        dis_y = self.food_y - y
        if dis_x < 0 and dis_y < 0:
            state.append(0)
        elif dis_x < 0 and dis_y == 0:
            state.append(1)
        elif dis_x < 0 and dis_y > 0:
            state.append(2)
        elif dis_x == 0 and dis_y > 0:
            state.append(3)
        elif dis_x > 0 and dis_y > 0:
            state.append(4)
        elif dis_x > 0 and dis_y == 0:
            state.append(5)
        elif dis_x > 0 and dis_y < 0:
            state.append(6)
        elif dis_x == 0 and dis_y < 0:
            state.append(7)
        elif dis_x == 0 and dis_y == 0:
            quit()
        node = []
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
        if y - 1 >= 0:
            node.append(self.board[x][y-1])
        else:
            node.append(TAIL)
        try:
            state.append(STATE_SPACE[str(node)])
        except KeyError:
            print(self.board)
            quit()
        return str(state)

    def get_action_dir(self, action):
        if action == 0:
            self.snake[0][2] = "↑"
        elif action == 1:
            self.snake[0][2] = "→"
        elif action == 2:
            self.snake[0][2] = "↓"
        elif action == 3:
            self.snake[0][2] = "←"

    def get_possible_actions(self):
        if self.snake[0][2] == "↑":
            return (0, 1, 3), 2
        elif self.snake[0][2] == "→":
            return (0, 1, 2), 3
        elif self.snake[0][2] == "↓":
            return (1, 2, 3), 0
        elif self.snake[0][2] == "←":
            return (0, 2, 3), 1

    def reset(self):
        self.over = False
        self.out = False
        self.snake.clear()
        self.board = np.zeros((BOARD_COUNT, BOARD_COUNT), dtype=int)
        d = np.random.randint(1, 5)
        if d == 1:
            ldir = "↓"
            x = np.random.randint(2, BOARD_COUNT - 1)
            x_1 = x - 1
            x_2 = x_1 - 1
            y = np.random.randint(0, BOARD_COUNT - 1)
            y_1 = y
            y_2 = y_1
        elif d == 2:
            ldir = "→"
            y = np.random.randint(2, BOARD_COUNT - 1)
            y_1 = y - 1
            y_2 = y_1 - 1
            x = np.random.randint(0, BOARD_COUNT - 1)
            x_1 = x
            x_2 = x_1
        elif d == 3:
            ldir = "↑"
            x = np.random.randint(0, BOARD_COUNT - 3)
            x_1 = x + 1
            x_2 = x_1 + 1
            y = np.random.randint(0, BOARD_COUNT - 1)
            y_1 = y
            y_2 = y_1
        elif d == 4:
            ldir = "←"
            x = np.random.randint(0, BOARD_COUNT - 1)
            x_1 = x
            x_2 = x_1
            y = np.random.randint(0, BOARD_COUNT - 3)
            y_1 = y + 1
            y_2 = y_1 + 1
        self.board[x][y] = HEAD
        self.board[x_1][y_1] = TAIL
        self.board[x_2][y_2] = TAIL
        self.snake.append([x, y, ldir])
        self.snake.append([x_1, y_1, ldir])
        self.snake.append([x_2, y_2, ldir])
        self.create_food()
        # self.dis_diff = self.get_dis()
        return self.get_state()

    def draw_snake(self, block_s, index):
        x = block_s[0]
        y = block_s[1]
        if block_s[2] == "↑":
            if index == 0:
                if x == 0 or self.board[x-1][y] == TAIL:
                    self.out = True
                else:
                    self.board[x-1][y] = HEAD
                    block_s[0] -= 1
            else:
                self.board[x-1][y] = TAIL
                block_s[0] -= 1
        elif block_s[2] == "↓":
            if index == 0:
                if x == BOARD_COUNT - 1 or self.board[x+1][y] == TAIL:
                    self.out = True
                else:
                    self.board[x+1][y] = HEAD
                    block_s[0] += 1
            else:
                self.board[x+1][y] = TAIL
                block_s[0] += 1
        elif block_s[2] == "←":
            if index == 0:
                if y == 0 or self.board[x][y-1] == TAIL:
                    self.out = True
                else:
                    self.board[x][y-1] = HEAD
                    block_s[1] -= 1
            else:
                self.board[x][y-1] = TAIL
                block_s[1] -= 1
        elif block_s[2] == "→":
            if index == 0:
                if y == BOARD_COUNT - 1 or self.board[x][y+1] == TAIL:
                    self.out = True
                else:
                    self.board[x][y+1] = HEAD
                    block_s[1] += 1
            else:
                self.board[x][y+1] = TAIL
                block_s[1] += 1
        if index == len(self.snake) - 1:
            self.board[x][y] = 0
        return block_s

    def draw_game(self, board):
        score = len(self.snake) - 3
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
        score_str = self.font.render(f"Score: {score}", 1, WHITE)
        self.win.blit(score_str, (240, 540))
        food_drawn = False
        for i in range(BOARD_COUNT):
            for j in range(BOARD_COUNT):
                if board[i][j] == HEAD:
                    pygame.draw.rect(self.win, YELLOW,
                                     (self.vel*j+21, self.vel*i+21,
                                      self.shape, self.shape))
                elif board[i][j] == TAIL:
                    pygame.draw.rect(self.win, RED,
                                     (self.vel*j+21, self.vel*i+21,
                                      self.shape, self.shape))
                elif board[i][j] == FOOD:
                    food_drawn = True
                    pygame.draw.rect(self.win, GREEN,
                                     (self.vel*j+21, self.vel*i+21,
                                      self.shape, self.shape))
        self.draw_win()
        pygame.display.flip()
        self.clock.tick(self.fps)
        if not food_drawn:
            print('[WARNING FOOD NOT FOUND]', self.food_hit)

    def draw_win(self):
        win_x = self.snake[0][0] - WINDOW_SIZE//2
        win_y = self.snake[0][1] - WINDOW_SIZE//2
        end_x = win_x + WINDOW_SIZE
        end_y = win_y + WINDOW_SIZE
        pygame.draw.line(self.win, WHITE,
                         (win_y*self.vel+21, win_x*self.vel+21),
                         (win_y*self.vel+21, end_x*self.vel+21))
        pygame.draw.line(self.win, WHITE,
                         (win_y*self.vel+21, win_x*self.vel+21),
                         (end_y*self.vel+21, win_x*self.vel+21))
        pygame.draw.line(self.win, WHITE,
                         (end_y*self.vel+21, win_x*self.vel+21),
                         (end_y*self.vel+21, end_x*self.vel+21))
        pygame.draw.line(self.win, WHITE,
                         (win_y*self.vel+21, end_x*self.vel+21),
                         (end_y*self.vel+21, end_x*self.vel+21))

    def handle_event(self):
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
                    self.fps += 1
                elif event.key == pygame.K_DOWN:
                    self.fps -= 1

    def create_food(self):
        while True:
            self.food_x = np.random.randint(0, BOARD_COUNT - 1)
            self.food_y = np.random.randint(0, BOARD_COUNT - 1)
            if self.board[self.food_x][self.food_y] == EMPTY:
                self.board[self.food_x][self.food_y] = FOOD
                break

    def add_tail(self):
        tail = self.snake[-1].copy()
        if tail[2] == "↑":
            tail[0] += 1
        elif tail[2] == "↓":
            tail[0] -= 1
        elif tail[2] == "←":
            tail[1] += 1
        elif tail[2] == "→":
            tail[1] -= 1
        if self.board[tail[0], tail[1]] != EMPTY:
            print("Can't add tail")
            print(self.snake[0])
            print(tail)
            print(self.food_x, self.food_y)
            print(self.board)
            quit()
        self.board[tail[0]][tail[1]] = TAIL
        self.snake.append(tail)

    def food_check(self):
        if self.snake[0][0] == self.food_x and self.snake[0][1] == self.food_y:
            self.food_hit = True
            self.add_tail()
            self.create_food()

    @staticmethod
    def caption(msg):
        pygame.display.set_caption(msg)

    def check_snake(self):
        for i, item in enumerate(self.snake):
            for j, item_j in enumerate(self.snake):
                if i == j:
                    pass
                else:
                    if item[0] == item_j[0] and item[1] == item_j[1]:
                        print("Snake broke")
                        print(self.snake)
                        print(self.board)
                        quit()
