from snake_game import Game
from tkinter import Tk, filedialog
import numpy as np
import json
tk_root = Tk()
tk_root.withdraw()
dir_name = filedialog.askopenfilename()
try:
    data_file = open(dir_name, 'r')
    q_table = json.load(data_file)
except FileNotFoundError:
    quit()
game = Game()
missing_states = []
while game.run:
    state = game.reset()
    while not game.over:
        print(len(missing_states))
        if state not in q_table:
            missing_states.append(state)
            q_table[state] = [np.random.random(), np.random.random(),
                              np.random.random(), np.random.random()]
            break
        game.get_window()
        action = np.argmax(q_table[state])
        over, n_state, reward = game.step(action)
        state = n_state
for item in missing_states:
    print(item)
