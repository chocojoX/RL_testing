import numpy as np


def play_order_preflop(players, button_pos):
    n = len(players)
    return([(button_pos+i+3)%n for i in range(n)])


def play_order_postflop(players, button_pos):
    n = len(players)
    return([(button_pos+i+1)%n for i in range(n)])
