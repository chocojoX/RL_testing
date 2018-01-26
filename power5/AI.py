import numpy as np
import cv2
import copy
import time
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.optimizers import SGD, Adadelta


def player_number(player):
    if player==1:
        return 1
    elif player==2:
        return -1
    else:
        return 1/0


class AI(object):
    def __init__(self, mode="NN", size=10, player=1, load=True, model_file="models/my_model.h5", random=True):

        self.mode = mode
        self.player=player
        self.model_file = model_file
        self.random=random
        self.size=size

        if load:
            self.load_model()

        if self.mode=="NN" and load==False:
            self.define_model()
            self.save_model()


    def play(self, power5):
        if self.mode=="random":
            return self.random_play(power5)
        elif self.mode == "NN":
            return self.NN_play(power5)
        else:
            print("No other AI than random and NN")
        pass


    def random_play(self, power5):
        legal_moves = power5.legal_moves
        move = np.random.randint(len(legal_moves))
        move = legal_moves[move]
        return move


    def NN_play(self, power5):
        legal = power5.legal_moves
        all_scores = []
        board = power5.game

        all_boards=[]
        for i, pos in enumerate(legal):
            board_tmp = player_number(self.player) * board.reshape(board.shape[0], board.shape[1], 1)[: , :, :]
            board_tmp[pos[0], pos[1], :] = 1
            all_boards.append(board_tmp)

        scores = self.model.predict(np.array(all_boards))
        if self.random:
            proba = (np.exp(10*scores) / (np.sum(np.exp(10*scores))))[:, 0]
            idx = np.random.choice(len(legal), 1,  p=proba)[0]
        else:
            idx = np.argmax(scores)
        return legal[idx]

    def define_model(self):
        input_shape = (self.size, self.size, 1)
        self.model = Sequential()
        self.model.add(Conv2D(20, (5, 5), padding='same', activation='sigmoid', input_shape=input_shape))
        # self.model.add(Dropout(0.25))

        self.model.add(Conv2D(16, (4, 4), kernel_initializer='random_uniform', padding='same', activation='sigmoid'))
        # self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        self.model.add(Flatten())
        self.model.add(Dense(12, kernel_initializer='random_uniform', activation='relu'))
        self.model.add(Dense(1, activation='sigmoid'))
        self.model.compile(loss='mse', optimizer='sgd')
        # self.save_model()

    def save_model(self):
        self.model.save(self.model_file)

    def load_model(self):
        self.model = load_model(self.model_file)
