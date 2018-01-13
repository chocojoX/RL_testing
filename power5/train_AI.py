import numpy as np
from power5 import Power5
from AI import AI
from game import Game
from keras.models import load_model
import copy


def get_smmetrical_positions(positions, score):
    horizontal_sym = positions[:, ::-1, :, :]
    vertical_sym = positions[:, :, ::-1, :]
    transposed_pos = positions.transpose(0,2,1,3)
    horizontal_transposed = horizontal_sym.transpose(0,2,1,3)
    vertical_transpose = vertical_sym.transpose(0,2,1,3)
    transpose_vertical = transposed_pos[:, :, ::-1, :]
    transpose_horizontal = transposed_pos[:,::-1, :, :]
    all_positions = np.concatenate((positions, horizonta, vertical_sym, transposed_pos, horizontal_transposed, vertical_transpose, transpose_vertical, transpose_horizontal), axis=0)
    all_scores = np.concatenate([score]*8)

    return all_positions, all_scores


class Trainer(object):
    def __init__(self, model_file):
        self.positions = []
        self.scores = []
        self.gamma = 0.2
        self.model_file=model_file
        self.model = load_model(self.model_file)


    def run_game(self, players, size=10, display=False, save_positions=True):
        game = Game(size, auto=True, display=False, training=True, players=players)
        positions, winner = game.run()
        if winner==1:
            score=1
        if winner==2:
            score=-1
        else:
            score=0

        if save_positions:
            for i, pos in enumerate(positions):
                n=len(positions)-1
                if np.abs(score)*self.gamma**(n-i)>0.01:
                    # print(score*self.gamma**(n-i))
                    self.positions.append(pos)
                    self.scores.append(score*self.gamma**(n-i))
        return winner

    def run_generation(self, n_games=100, size=10, display=False, save_model_path="models/trained.h5"):
        ai1 = AI(mode="NN", size =10, player=1, load=True, model_file=self.model_file)
        ai2 = AI(mode="NN", size =10, player=2, load=True, model_file=self.model_file)
        for i in range(n_games):
            self.run_game(size=10, players=[ai1, ai2])

        self.positions = np.array(self.positions).reshape(len(self.positions), size, size, 1)
        self.scores = np.array(self.scores)

        self.model= load_model(self.model_file)
        import pdb; pdb.set_trace()
        self.model.fit(self.positions, self.scores, epochs=10, batch_size=300)
        self.model.save(save_model_path)


    def test_model_vs_random(self, n_games=100, size=10, display=False, model_path="models/trained.h5"):
        ai1 = AI(mode="NN", size =10, player=1, load=True, model_file=model_path)
        ai2 = AI(mode="random", size =10, player=2)

        nb_wins = 0
        nb_losses = 0
        nb_draws = 0

        for i in range(n_games):
            winner = self.run_game(size=10, players=[ai1, ai2], save_positions=False)
            if winner==1:
                nb_wins+=1
            elif winner==2:
                nb_losses+=1
            else:
                nb_draws+=1
        print("Model won %i games, lost %i and drawn %i against random (out of %i games)" %(nb_wins, nb_losses, nb_draws, n_games))


    def run(self, n_generation, n_games=1000, size=10, display=False):
        for gen in range(n_generation):
            self.positions = []
            self.scores = []
            save_model_path = "models/trained_ultra_soft_generation%i.h5"%(gen)
            print("Generation %i training..."%(gen))
            self.run_generation(n_games=n_games, size=size, display=display, save_model_path=save_model_path)
            self.model_file = save_model_path
            print("Generation %i testing vs random..."%(gen))
            self.test_model_vs_random(n_games=30, size=10, display=False, model_path=self.model_file)




if __name__ == "__main__":
    ai = AI(load=False)
    T = Trainer(model_file="models/my_model.h5")
    T.run(n_generation=20)
    T.test_model_vs_random(model_path="models/trained.h5")
    pass
