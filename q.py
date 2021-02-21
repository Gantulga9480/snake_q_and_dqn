from snake_game import *
import numpy as np
import time
import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--index', default='')
args = parser.parse_args()


LR = 0.001
GAMMA = 0.999
EPSILON = 1
EPSILON_MIN = 0
EPSILON_DECAY = 0.999999
MAX_REWARD = 4000

q_table = {}

# time.sleep(1)
game = Game()
show_every = 100
ep_rewards = []
reward_tmp = 0

episode = 0
while game.run:
    ep_r = 0
    action_counter = 0
    state = game.reset()
    while not game.over:
        if np.random.random() > EPSILON:
            if state in q_table:
                p_actions, imp = game.get_possible_actions()
                action_values = q_table[state].copy()
                action_values[imp] = OUT_REWARD * 4
                action = np.argmax(q_table[state])
            else:
                q_table[state] = [0, 0, 0, 0]
                p_actions, imp = game.get_possible_actions()
                action = p_actions[np.random.randint(3)]
        else:
            if state not in q_table:
                q_table[state] = [0, 0, 0, 0]
            p_actions, _ = game.get_possible_actions()
            action = p_actions[np.random.randint(3)]
        EPSILON = 0 if EPSILON < 0.01 else EPSILON * EPSILON_DECAY
        _, n_state, reward = game.step(action)
        if n_state not in q_table:
            q_table[n_state] = [0, 0, 0, 0]
        ep_r += reward
        action_counter += 1
        if action_counter > 100 and EPSILON <= 0.01:
            game.over = True
        if reward == FOOD_REWARD:
            action_counter = 0
        if not game.over:
            max_future_q_value = np.max(q_table[n_state])
            current_q_value = q_table[state][action]
            new_q_value = current_q_value + LR * \
                (reward + GAMMA*max_future_q_value - current_q_value)
            q_table[state][action] = new_q_value
        elif game.over:
            q_table[state][action] = reward
        state = n_state
    ep_rewards.append(ep_r)
    episode += 1
    if episode % show_every == 0:
        avg_r = sum(ep_rewards) / show_every
        ep_rewards.clear()
        if avg_r > reward_tmp:
            desc = f'{LR} - avg: ↑ {avg_r} ep: {episode}'
        elif avg_r == reward_tmp:
            desc = f'{LR} - avg: = {avg_r} ep: {episode}'
        else:
            desc = f'{LR} - avg: ↓ {avg_r} ep: {episode}'
        desc += f' eps: {EPSILON} state: {len(q_table)}'
        reward_tmp = avg_r
        game.caption(desc)
        if avg_r >= MAX_REWARD:
            MAX_REWARD = avg_r
            with open(f'data{args.index}_{avg_r}.json', 'w') as fp:
                json.dump(q_table, fp)
with open(f'data{args.index}.json', 'w') as fp:
    json.dump(q_table, fp)
