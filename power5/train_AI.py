import numpy as np
from power5 import Power5
from AI import AI
from game import Game
from keras.models import load_model


class Trainer(object):
    def __init__(self, model_file):
        self.positions = []
        self.scores = []
        self.gamma = 0.8
        self.model_file=model_file
        self.model = load_model(self.model_file)


    def run_game(self, size=10, display=False):
        game = Game(size, auto=True, display=False, training=True)
        positions, winner = game.run()
        if winner==1:
            score=1
        if winner==2:
            score=-1
        else:
            score=0

        for i, pos in enumerate(positions):
            n=len(positions)-1
            self.positions.append(pos)
            self.scores.append(score*self.gamma**(n-i))

    def run(self, n_games=2, size=10, display=False):
        for i in range(n_games):
            print(i)
            self.run_game(size=10)

        self.positions = np.array(self.positions).reshape(len(self.positions), size, size, 1)
        self.scores = np.array(self.scores)
        self.model.fit(self.positions, self.scores, epochs=10, batch_size=32)
        self.model.save("models/trained.h5")





if __name__ == "__main__":
    T = Trainer(model_file="models/my_model.h5")
    T.run()
    pass
