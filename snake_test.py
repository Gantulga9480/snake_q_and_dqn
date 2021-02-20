from snake_game import Game
import numpy as np
try:
    q_table = np.load('model_1.npy')
except FileNotFoundError:
    quit()
game = Game()
while game.run:
    state = game.reset()
    while not game.over:
        action = np.argmax(q_table[state[0], state[1], state[2], state[3],
                           state[4]])
        over, n_state, reward = game.step(action)
        state = n_state
