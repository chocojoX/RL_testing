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
            if self.cards[card] == "deck":
                card1 = card
                self.cards[card] = player.get_id()

        card2 = None
        while card2 is None:
            card = np.random.choice(cards, 1)[0]
            if self.cards[card] == "deck":
                card2 = card
                self.cards[card] = player.get_id()
        player.deal_cards(card1, card2)
        return [card1, card2]


    def deal_flop(self):
        flop = []
        cards = [*self.cards]   #List of the keys of the dictionnary
        for i in range(3):
            card1 = None
            while card1 is None:
                card = np.random.choice(cards, 1)[0]
                if self.cards[card] == "deck":
                    card1 = card
                    self.cards[card] = "flop"
                    flop.append(card)
        return flop


    def deal_river(self):
        cards = [*self.cards]   #List of the keys of the dictionnary
        card1 = None
        while card1 is None:
            card = np.random.choice(cards, 1)[0]
            if self.cards[card] == "deck":
                card1 = card
                self.cards[card] = "river"
        return card


    def deal_turn(self):
        cards = [*self.cards]   #List of the keys of the dictionnary
        card1 = None
        while card1 is None:
            card = np.random.choice(cards, 1)[0]
            if self.cards[card] == "deck":
                card1 = card
                self.cards[card] = "turn"
        return card
