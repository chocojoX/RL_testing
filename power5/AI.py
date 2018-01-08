import numpy as np
import cv2
import copy
from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.optimizers import SGD, Adadelta



class AI(object):
    def __init__(self, mode="NN", size =10, player=1):

        self.mode = mode
        self.player=player

        if self.mode=="NN":
            input_shape = (size, size, 1)
            self.model = Sequential()
            self.model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=input_shape))
            self.model.add(Conv2D(32, (3, 3), kernel_initializer='random_uniform', activation='relu'))
            self.model.add(MaxPooling2D(pool_size=(2, 2)))
            self.model.add(Dropout(0.25))

            self.model.add(Conv2D(64, (3, 3), kernel_initializer='random_uniform', padding='same', activation='relu'))
            self.model.add(Conv2D(64, (3, 3), kernel_initializer='random_uniform', activation='relu'))
            self.model.add(MaxPooling2D(pool_size=(2, 2)))
            self.model.add(Dropout(0.25))

            self.model.add(Flatten())
            self.model.add(Dense(8, kernel_initializer='random_uniform', activation='relu'))
            self.model.add(Dropout(0.5))
            self.model.add(Dense(1, activation='linear'))
            self.model.compile(loss='mean_squared_error', optimizer='sgd')


    def play(self, power5):
        if self.mode=="random":
            return self.random_play(power5)
        elif self.mode == "NN":
            return self.NN_play(power5)
        else:
            print("No other AI than random")
        pass


    def random_play(self, power5):
        legal_moves = power5.legal_moves
        move = np.random.randint(len(legal_moves))
        move = legal_moves[move]
        return move


    def NN_play(self, power5):
        legal = power5.legal_moves
        best_score = -100000000
        idx = -1
        board = power5.game

        for i, pos in enumerate(legal):
            board_tmp = copy.deepcopy(board).reshape(board.shape[0], board.shape[1], 1)[None, : , :, :]
            board_tmp[:, pos[0], pos[1], :] = self.player
            score = self.model.predict(board_tmp)
            if score>best_score:
                idx = i
                best_score=score
        return legal[idx]
