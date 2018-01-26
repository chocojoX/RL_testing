import power5, board
import numpy as np
import cv2
import copy
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import time
from AI import AI


def switch_player(player):
    if player==1:
        return 2
    return 1


class Game(object):
    def __init__(self, size, auto, display, training=False, players = ["human", "human"]):
        self.size = size
        self.auto = auto
        self.training=training
        self.players = players
        self.delay_win=10000

        self.display=display
        self.game = power5.Power5(self.size, display=display)
        cv2.namedWindow('Power5')
        if self.training:
            self.delay_win = 1
        if not self.auto:
            cv2.setMouseCallback('Power5', self.mouse_event)


    def reinit(self):
        self.game = power5.Power5(self.size, display=self.display)
        cv2.namedWindow('Power5')


    def run(self):
        positions = []
        self.player = 1
        self.winner=0
        finished=False
        while not finished:
            if self.display:
                render = self.game.board.background
                cv2.imshow("Power5", render)
                k = cv2.waitKey(30) & 0xFF
                if k==27:
                    break
            if self.players[self.player-1]!="human":
                if self.player==1:
                    x, y = self.players[0].play(self.game)
                else:
                    x, y = self.players[1].play(self.game)
                if self.game.is_move_legal((x,y)):
                    self.game.move(self.player, (x, y))

                if self.game.check_victory(self.player, (x, y)):
                    self.winner = self.player
                    finished=True
                    if self.display:
                        self.display_end_of_game()
                if self.game.is_draw():
                    self.winner = 0
                    finished=True
                    if self.display:
                        self.display_end_draw()
                self.player = switch_player(self.player)
                positions.append(copy.deepcopy(self.game.game))
        if self.training:
            return positions, self.winner


    def mouse_event(self, event, mx, my, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and self.players[self.player-1]=="human":
            click = [mx, my]
            square_size = self.game.board.square_size
            x = int(mx/square_size)
            y = int(my/square_size)
            if self.game.is_move_legal((x,y)):
                self.game.move(self.player, (x, y))

            if self.game.check_victory(self.player, (x, y)):
                self.display_end_of_game()
            self.player = switch_player(self.player)

    def display_end_of_game(self):
        message = "Player %i wins !" %(self.player)
        cv2.putText(self.game.board.background, message, (int(0.1*self.game.board.length), int(0.5*self.game.board.length)), 0, 2, [150,150,150], 3)
        cv2.imshow("Power5", self.game.board.background)
        cv2.waitKey(self.delay_win)
        self.reinit()


    def display_end_draw(self):
        message = "Draw !"
        cv2.putText(self.game.board.background, message, (int(0.1*self.game.board.length), int(0.5*self.game.board.length)), 0, 2, [150,150,150], 3)
        cv2.imshow("Power5", self.game.board.background)
        cv2.waitKey(self.delay_win)
        self.reinit()



if __name__ == "__main__":
    # parse args
    description = "Power5. Line up 5 pawns in a row and you win. "
    parser = ArgumentParser(description=description, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--size", type=int , default=10, help="Size of board in pixels")
    parser.add_argument("-a", "--auto", action='store_true', default=False, help="Computer plays itself")
    args = parser.parse_args()
    # launch game
    game = Game(args.size, args.auto, display=True)
    game.run()
