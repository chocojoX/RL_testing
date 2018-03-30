import numpy as np


class Deck(object):
    def __init__(self):
        self.colors = ["H", "D", "S", "C"]
        self.cards = {}
        for i in range(13):
            for col in self.colors:
                self.cards[str(i)+col] = "deck"


    def reset(self):
        for key in self.cards.keys():
            self.cards[key] = "desk"


    def deal_player(self, player):
        cards = [*self.cards]   #List of the keys of the dictionnary
        card1 = None
        while card1 is None:
            card = np.random.choice(cards, 1)[0]
            if self.cards[card] != "deck":
                card1 = card
                self.cards[card] = player.get_id()


    def deal_card_to_player(self, card, player_id):
        self.cards[card] = player_id


    def deal_card_to_flop(self, card):
        self.cards[card] = "flop"


    def deal_card_to_river(self, card):
        self.cards[card] = "river"


    def deal_card_to_turn(self, card):
        self.cards[card] = "turn"
