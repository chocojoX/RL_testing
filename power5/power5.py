import copy
from board import *


class Power5(object):
    def __init__(self, size=10, display=True):
        self.size = size
        self.board = Power5_Board(size=size)
        self.game = np.zeros((size, size))
        self.display=display


    def is_move_legal(self, pos):
        if self.game[pos[0], pos[1]]==0:
            return True
        else:
            return False
            

    def move(self, player, pos):
        if self.is_move_legal(pos):
            self.game[pos[0], pos[1]]=player
            if player==1:
                self.board.draw_circle(pos)
            if player==2:
                self.board.draw_cross(pos)
            return True
        else:
            return False

    def check_victory(self, player, pos):
        # Horizontal checking
        consecutive = 1
        for i in [-4, -3, -2, -1, 1, 2, 3, 4]:
            if pos[0]+i>=0 and pos[0]+i<self.size:
                if self.game[pos[0]+i, pos[1]]==player:
                    consecutive += 1
                else:
                    consecutive = 1
                if consecutive == 5:
                    return True
        # Vertical checking
        for i in [-4, -3, -2, -1, 1, 2, 3, 4]:
            if pos[1]+i>=0 and pos[1]+i<self.size:
                if self.game[pos[0], pos[1]+i]==player:
                    consecutive += 1
                else:
                    consecutive = 1
                if consecutive == 5:
                    return True
        # Up-Down Diagonal
        for i in [-4, -3, -2, -1, 1, 2, 3, 4]:
            if pos[0]+i>=0 and pos[0]+i<self.size and pos[1]+i>=0 and pos[1]+i<self.size:
                if self.game[pos[0]+i, pos[1]+i]==player:
                    consecutive += 1
                else:
                    consecutive = 1
                if consecutive == 5:
                    return True
        # Down-Up Diagonal
        for i in [-4, -3, -2, -1, 1, 2, 3, 4]:
            if pos[0]-i>=0 and pos[0]-i<self.size and pos[1]-i>=0 and pos[1]-i<self.size:
                if self.game[pos[0]-i, pos[1]-i]==player:
                    consecutive += 1
                else:
                    consecutive = 1
                if consecutive == 5:
                    return True
        return False

    def is_draw(self):
        return np.sum(np.abs(self.game)) == self.size**2
