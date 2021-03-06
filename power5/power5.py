import copy
from board import *


def initialize_legal_moves(size):
    legal = []
    for i in range(size):
        for j in range(size):
            legal.append((i, j))
    return legal


def player_number(player):
    if player==1:
        return 1
    elif player==2:
        return -1
    else:
        return 1/0



class Power5(object):
    def __init__(self, size=10, display=True):
        self.size = size
        self.board = Power5_Board(size=size)
        self.game = np.zeros((size, size))
        self.display=display
        self.legal_moves = initialize_legal_moves(size)


    def is_move_legal(self, pos):
        if self.game[pos[0], pos[1]]==0:
            return True
        else:
            return False


    def move(self, player, pos):
        if self.is_move_legal(pos):
            self.game[pos[0], pos[1]]=player_number(player)
            if player==1:
                if self.display:
                    self.board.draw_circle(pos)
                self.legal_moves = [lpos for lpos in self.legal_moves if lpos!=pos]
            if player==2:
                if self.display:
                    self.board.draw_cross(pos)
                self.legal_moves = [lpos for lpos in self.legal_moves if lpos!=pos]
            return True
        else:
            return False


    def check_victory(self, player, pos):
        # Horizontal checking
        consecutive = 1
        for i in [-4, -3, -2, -1, 1, 2, 3, 4]:
            if pos[0]+i>=0 and pos[0]+i<self.size:
                if self.game[pos[0]+i, pos[1]]==player_number(player):
                    consecutive += 1
                else:
                    consecutive = 1
                if consecutive == 5:
                    return True
        # Vertical checking
        for i in [-4, -3, -2, -1, 1, 2, 3, 4]:
            if pos[1]+i>=0 and pos[1]+i<self.size:
                if self.game[pos[0], pos[1]+i]==player_number(player):
                    consecutive += 1
                else:
                    consecutive = 1
                if consecutive == 5:
                    return True
        # Up-Down Diagonal
        for i in [-4, -3, -2, -1, 1, 2, 3, 4]:
            if pos[0]+i>=0 and pos[0]+i<self.size and pos[1]+i>=0 and pos[1]+i<self.size:
                if self.game[pos[0]+i, pos[1]+i]==player_number(player):
                    consecutive += 1
                else:
                    consecutive = 1
                if consecutive == 5:
                    return True
        # Down-Up Diagonal
        for i in [-4, -3, -2, -1, 1, 2, 3, 4]:
            if pos[0]-i>=0 and pos[0]-i<self.size and pos[1]+i>=0 and pos[1]+i<self.size:
                if self.game[pos[0]-i, pos[1]+i]==player_number(player):
                    consecutive += 1
                else:
                    consecutive = 1
                if consecutive == 5:
                    return True
        return False

    def is_draw(self):
        return len(self.legal_moves)==0
