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


    def deal_cards(self, card1, card2):
        self.cards = [card1, card2]


    def print_cards(self):
        if len(self.cards)==2:
            to_print = ""
            for i, card in enumerate(self.cards):
                height = int(card[:-1])
                color = card[-1]
                if height == 1:
                    height = "A"
                if height==11:
                    height = "J"
                elif height==12:
                    height = "Q"
                elif height == 13:
                    height = "K"
                to_print = to_print + str(height) + " " + color
                if i==0 :
                    to_print = to_print + " -- "
            print(to_print)
        else:
            print("Player %i has no cards in hand" %(self.id))

    def act(self, state):
        pass


    def random_play(self, bb, state):
        p_check_fold = 0.5
        p_call = 0.3
        pass
