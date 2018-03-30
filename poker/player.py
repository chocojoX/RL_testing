import numpy as np


class Player(object):
    def __init__(self, stack=1000, id=None):
        self.stack = stack
        self.cards = []
        self.id = id
        pass

    def reset_hand(self):
        self.cards = []


    def get_id(self):
        return self.id

    def random_play(self, bb, state):
        p_check_fold = 0.5
        p_call = 0.3
