from snake_game import *
import numpy as np
import time
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--index', default='')
args = parser.parse_args()


LR = 0.1
GAMMA = 0.99
EPSILON = 1
EPSILON_MIN = 0.1
EPSILON_DECAY = 0.99999999

# ep_decay: 0.99999999

try:
    q_table = np.load(f'model_{args.index}.npy')
    print('Loading pre trained model')
except FileNotFoundError:
    q_table = np.zeros((20, 20, 20, 20, 43, 4), dtype=float)
    print('Creating new model')
time.sleep(1)

game = Game()
show_every = 500
ep_rewards = []
reward_tmp = 0

episode = 0
while game.run:
    ep_r = 0
    state = game.reset()
    while not game.over:
        if np.random.random() > EPSILON:
            p_actions, imp = game.get_possible_actions()
            action_values = q_table[state[0], state[1], state[2], state[3],
                                    state[4]]
            action_values[imp] = OUT_REWARD * 4
            action = np.argmax(action_values)
        else:
            p_actions, _ = game.get_possible_actions()
            action = p_actions[np.random.randint(3)]
            EPSILON = max(EPSILON * EPSILON_DECAY, EPSILON_MIN)
        over, n_state, reward = game.step(action)
        ep_r += reward
        if not over:
            max_future_q_value = np.max(q_table[n_state[0], n_state[1],
                                        n_state[2], n_state[3], state[4]])
            current_q_value = q_table[state[0], state[1],
                                      state[2], state[3], state[4], action]
            new_q_value = current_q_value+LR *\
                (reward+GAMMA*max_future_q_value-current_q_value)
            q_table[state[0], state[1], state[2],
                    state[3], state[4], action] = new_q_value
        elif over:
            q_table[state[0], state[1], state[2], state[3], action] = reward
        state = n_state
    ep_rewards.append(ep_r)
    episode += 1
    if episode % show_every == 0:
        avg_r = sum(ep_rewards) / show_every
        ep_rewards.clear()
        if avg_r > reward_tmp:
            desc = f'{LR} - avg: ↑ {avg_r} ep: {episode} eps: {EPSILON}'
        else:
            desc = f'{LR} - avg: ↓ {avg_r} ep: {episode} eps: {EPSILON}'
        game.caption(desc)
        reward_tmp = avg_r
np.save(f'model_{args.index}.npy', q_table)
