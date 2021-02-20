from snake_game import Game
import numpy as np
import random
from collections import deque
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import mixed_precision

BUFFER_SIZE = 10000
MIN_BUFFER_SIZE = 2000
BATCH_SIZE = 32
EPOCH = 1
DISCOUNT_RATE = 0.99
LEARNING_RATE = 0.001
EPSILON = 1
MIN_EPSILON = 0.1
EPSILON_DECAY = .99999999
TARGET_NET_UPDATE_FREQUENCY = 30

REPLAY_BUFFER = deque(maxlen=BUFFER_SIZE)
SAMPLES = list()

FRAME = 1
EPISODE = 1
UPDATE_COUNTER = 1


class MyCallback(keras.callbacks.Callback):

    def on_epoch_end(self, epoch, logs=None):
        if logs.get('accuracy') > 0.95:
            print("Reached 95% accuracy so cancelling training!")
            self.model.stop_training = True


def get_model():
    model = Sequential()
    model.add(Input(shape=(5,), name='input'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(4))
    model.add(Activation('linear', dtype='float32'))
    model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE),
                  metrics=["accuracy"])
    model.summary()
    return model


def keras_train():
    SAMPLES = random.sample(REPLAY_BUFFER, BATCH_SIZE)
    current_states = np.array([item[0] for item in SAMPLES])
    new_current_state = np.array([item[2] for item in SAMPLES])
    current_qs_list = []
    future_qs_list = []
    current_qs_list = main_nn.predict(current_states)
    future_qs_list = target_nn.predict(new_current_state)

    X = []
    Y = []
    for index, (state, action, _, reward, done) in enumerate(SAMPLES):
        if not done:
            new_q = reward + DISCOUNT_RATE * np.max(future_qs_list[index])
        else:
            new_q = reward

        current_qs = current_qs_list[index]
        current_qs[action] = new_q

        X.append(state)
        Y.append(current_qs)
    main_nn.fit(np.array(X), np.array(Y), epochs=EPOCH,
                batch_size=BATCH_SIZE, shuffle=False,
                verbose=0, callbacks=[callbacks])


policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_global_policy(policy)
print('Compute dtype: %s' % policy.compute_dtype)
print('Variable dtype: %s' % policy.variable_dtype)

main_nn = get_model()
target_nn = get_model()
target_nn.set_weights(main_nn.get_weights())
callbacks = MyCallback()

game = Game()
show_every = 10
ep_rewards = []
reward_tmp = 0

while game.run:
    state = game.reset()
    terminal = False
    ep_reward = 0
    while not game.over:
        FRAME += 1
        if np.random.random() < EPSILON:
            action = np.random.randint(4)
            EPSILON = max(EPSILON * EPSILON_DECAY, MIN_EPSILON)
        else:
            action = np.argmax(main_nn.predict(np.expand_dims(state, axis=0)))
        terminal, new_state, r = game.step(action=action)
        ep_reward += r
        REPLAY_BUFFER.append([state, action, new_state, r, terminal])
        state = new_state

        if terminal and len(REPLAY_BUFFER) > MIN_BUFFER_SIZE:
            keras_train()
            UPDATE_COUNTER += 1

        if UPDATE_COUNTER % TARGET_NET_UPDATE_FREQUENCY == 0:
            target_nn.set_weights(main_nn.get_weights())
            UPDATE_COUNTER = 1
    ep_rewards.append(ep_reward)
    if EPISODE % show_every == 0:
        avg_r = sum(ep_rewards) / show_every
        ep_rewards.clear()
        if avg_r > reward_tmp:
            desc = f'avg: ↑ {avg_r} ep: {EPISODE} eps: {EPSILON}'
        else:
            desc = f'avg: ↓ {avg_r} ep: {EPISODE} eps: {EPSILON}'
        reward_tmp = avg_r
        game.caption(desc)
    EPISODE += 1

print("Training done congrat!!!")
# main_nn.save("main")
main_nn.save("main.h5")
# target_nn.save("target")
