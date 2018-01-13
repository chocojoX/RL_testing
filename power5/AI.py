import numpy as np
import cv2
import copy
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
    def __init__(self, mode="NN", size =10, player=1, load=True, model_file="models/my_model.h5"):

        self.mode = mode
        self.player=player
        self.model_file = model_file

        if load:
            self.load_model()

        if self.mode=="NN" and load==False:
            input_shape = (size, size, 1)
            self.model = Sequential()
            self.model.add(Conv2D(20, (5, 5), padding='same', activation='relu', input_shape=input_shape))
            # self.model.add(MaxPooling2D(pool_size=(2, 2)))
            # self.model.add(Dropout(0.25))

            # self.model.add(Conv2D(20, (5, 5), kernel_initializer='random_uniform', padding='same', activation='relu'))
            # self.model.add(MaxPooling2D(pool_size=(2, 2)))
            # self.model.add(Dropout(0.25))

            self.model.add(Flatten())
            self.model.add(Dense(4, kernel_initializer='random_uniform', activation='relu'))
            self.model.add(Dense(1, activation='linear'))
            self.model.compile(loss='mean_squared_error', optimizer='sgd')
            self.save_model()


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
        all_scores = []
        best_score = -100000000
        idx = -1
        board = power5.game

        all_boards=[]
        for i, pos in enumerate(legal):
            board_tmp = player_number(self.player) * board.reshape(board.shape[0], board.shape[1], 1)[: , :, :]
            board_tmp[pos[0], pos[1], :] = player_number(self.player)
            all_boards.append(board_tmp)
        scores = self.model.predict(np.array(all_boards))
        # all_scores.append(10*score)
        # if score>best_score:
        #     idx = i
        #     best_score=score
        proba = (np.exp(scores) / (np.sum(np.exp(scores))))[:, 0]
        idx = np.random.choice(len(legal), 1,  p=proba)[0]
        return legal[idx]

    def save_model(self):
        self.model.save(self.model_file)

    def load_model(self):
        self.model = load_model(self.model_file)
