import numpy as np
import cv2
import copy
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD, Adadelta



class AI(object):
    def __init__(self, mode="random", size =10):

        self.mode = mode

        if self.mode=="NN":
            self.model = Sequential()
            self.model.add(Convolution2D(64, 3, 3,
                                    border_mode='same', activation='relu',
                                    input_shape=(3, 256, 256)))
            # now self.model.output_shape == (None, 64, 256, 256)

            # add a 3x3 convolution on top, with 32 output filters:
            self.model.add(Convolution2D(32, 3, 3, border_mode='same', activation='relu'))

            # now model.output_shape == (None, 32, 256, 256)


    def play(self, power5):
        if self.mode=="random":
            return self.random_play(power5)
        else:
            print("No other AI than random")
        pass


    def random_play(self, power5):
        legal_moves = power5.legal_moves
        move = np.random.randint(len(legal_moves))
        move = legal_moves[move]
        return move
