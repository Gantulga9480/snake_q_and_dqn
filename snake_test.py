from snake_game import Game
import numpy as np
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--index', default='')
args = parser.parse_args()
try:
    q_table = np.load(f'model{args.index}.npy')
except FileNotFoundError:
    quit()
game = Game()
while game.run:
    state = game.reset()
    while not game.over:
        action = np.argmax(q_table[state[0], state[1]])
        over, n_state, reward = game.step(action)
        state = n_state
