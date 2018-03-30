import numpy as np


class Table(object):
    def __init__(self, players):
        self.players = players
        self.player_cards = [[] for p in self.players]
        self.public_cards = []


    def reset(self):
        self.player_cards = [[] for p in self.players]
        self.public_cards = []
