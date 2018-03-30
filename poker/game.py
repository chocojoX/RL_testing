from player import Player as Player
from deck import Deck as Deck
from table import Table as Table
from utils import *


class Game(object):
    def __init__(self, bb=20, ante=2, n_players=9, stack=3000):
        # Big blind
        self.bb = bb
        self.ante = 2
        # All players are AI for the moment
        self.players = [Player(stack=stack, id=i) for i in range(n_players)]
        self.deck = Deck()
        self.table = Table(players = self.players)
        self.status = "preflop"
        self.button_position = 0
        self.state = None # TODO : define the state as everything the players can see (history, pot, public cards...)


    def deal_to_players(self, verbose=0):
        for i, p in enumerate(self.players):
            cards = self.deck.deal_player(p)
            self.table.player_cards[i] = cards
            if verbose>1:
                p.print_cards()


    def deal_flop(self):
        flop = self.deck.deal_flop()
        self.table.public_cards = flop


    def deal_river(self):
        river = self.deck.deal_river()
        self.table.public_cards.append(river)
        pass


    def deal_turn(self):
        turn = self.deck.deal_turn()
        self.table.public_cards.append(turn)



    def play_hand(self):
        # TODO
        #Preflop
        self.deal_to_players()
        for i in play_order_preflop(self.players, self.button_position):
            p = self.players[i]
            decision = p.act(self.state)
            self.act(i, decision)
        #Flop
        self.deal_flop()
        for i in play_order_postflop(self.players, self.button_position):
            p = self.players[i]
            decision = p.act(self.state)
            self.act(i, decision)
        #River
        self.deal_river()
        for i in play_order_postflop(self.players, self.button_position):
            p = self.players[i]
            decision = p.act(self.state)
            self.act(i, decision)
        #Turn
        self.deal_turn()
        for i in play_order_postflop(self.players, self.button_position):
            p = self.players[i]
            decision = p.act(self.state)
            self.act(i, decision)

        print(self.table.public_cards)
        self.end_hand()


    def act(self, i, decision):
        #TODO change the state of the table according to the decision made by player i
        pass


    def end_hand(self):
        self.deck.reset()
        self.table.reset()
        for p in self.players:
            p.reset_hand()
        pass


if __name__=="__main__":
    g = Game()
    g.play_hand()
