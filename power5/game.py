import power5, board
import numpy as np
import cv2
import copy
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import time


def switch_player(player):
    if player==1:
        return 2
    return 1


class Game(object):
    def __init__(self, size, auto, write, display):
        self.size = size
        self.auto = auto
        self.display=display
        self.write = write
        self.game = power5.Power5(self.size, display=display)
        cv2.namedWindow('Power5')
        self.delay_win = 2000
        if not self.auto:
            cv2.setMouseCallback('Power5', self.mouse_event)


    def reinit(self):
        self.game = power5.Power5(self.size, display=self.display)
        cv2.namedWindow('Power5')


    def main(self):
        self.player = 1
        while True:
            # render
            render = self.game.board.background
            # show
            cv2.imshow("Power5", render)
            k = cv2.waitKey(30) & 0xFF
            if k==27:
                break


    def mouse_event(self, event, mx, my, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            click = [mx, my]
            square_size = self.game.board.square_size
            x = int(mx/square_size)
            y = int(my/square_size)
            if self.game.is_move_legal((x,y)):
                self.game.move(self.player, (x, y))

            if self.game.check_victory(self.player, (x, y)):
                message = "Player %i wins !" %(self.player)
                cv2.putText(self.game.board.background, message, (int(0.1*self.game.board.length), int(0.5*self.game.board.length)), 0, 2, [150,150,150], 3)
                cv2.imshow("Power5", self.game.board.background)
                cv2.waitKey(2000)
                self.reinit()
            self.player = switch_player(self.player)



if __name__ == "__main__":
    # parse args
    description = "Power5. Line up 5 pawns in a row and you win. "
    parser = ArgumentParser(description=description, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--size", type=int , default=10, help="Size of board in pixels")
    parser.add_argument("-w", "--write", type=str, default='', help="Write images in specified dir")
    parser.add_argument("-a", "--auto", action='store_true', default=False, help="Computer plays itself")
    args = parser.parse_args()
    # launch game
    game = Game(args.size, args.auto, args.write, display=True)
    game.main()
