import numpy as np
from power5 import Power5
from AI import AI
from game import Game
from keras.models import load_model
import copy
import sys
from scipy.stats import norm
import time


def get_symmetrical_positions(positions, score):
    horizontal_sym = positions[:, ::-1, :, :]
    vertical_sym = positions[:, :, ::-1, :]
    transposed_pos = positions.transpose(0,2,1,3)
    horizontal_transposed = horizontal_sym.transpose(0,2,1,3)
    vertical_transpose = vertical_sym.transpose(0,2,1,3)
    transpose_vertical = transposed_pos[:, :, ::-1, :]
    transpose_horizontal = transposed_pos[:,::-1, :, :]
    all_positions = np.concatenate((positions, horizontal_sym, vertical_sym, transposed_pos, horizontal_transposed, vertical_transpose, transpose_vertical, transpose_horizontal), axis=0)
    all_scores = np.concatenate([score]*8)

    return all_positions, all_scores


def convert_time(t):
    """ t is a duration in seconds, the function converts it to minutes, seconds"""
    minutes = int(t/60)
    seconds = int(t-60*minutes)
    return minutes, seconds



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
                    if i%2==1:
                        pos=-pos
                        self.scores.append(-score*self.gamma**(n-i))
                    else:
                        self.scores.append(score*self.gamma**(n-i))
                    self.positions.append(pos)
        return winner

    def run_generation(self, n_games=100, size=10, display=False, save_model_path="models/trained.h5", n_generation=0):
        ai1 = AI(mode="NN", size =10, player=1, load=True, model_file=self.model_file, random=False)
        ai2 = AI(mode="random", size =10, player=2, load=True, model_file=self.model_file)
        n_wins = 0.; n_finished=0; n_draws=0.; n_losses = 0.
        times = []

        ### Step 1 : playing against random
        print("Playing against random AI")
        for i in range(int(n_games/(n_generation+1))):
            t = time.time()
            winner = self.run_game(size=10, players=[ai1, ai2])
            n_finished+=1
            if winner==1:
                n_wins+=1
            elif winner==0:
                n_draws+=1
            else:
                n_losses+=1
            if i%10==9:
                times.append(time.time()-t)
                mean_score = n_wins/(n_wins+n_losses)
                sigma=0.5
                Sn = np.sqrt(n_wins+n_losses) * (np.abs(mean_score-0.5))/(sigma)
                gauss = norm()
                p = 2*(1-norm.cdf(Sn))

                minutes, sec = convert_time(np.mean(times[-10:])*(n_games-i)/10*len(times[-10:]))
                sys.stdout.write("\r Current score after %i games : %i/%i/%i, p value : %.3f, ETA : %i min %i s" % (n_finished, n_wins, n_draws, n_losses, p, minutes, sec))

        ### Step 1 : playing against random
        for gen in range(n_generation):
            n_wins = 0.; n_finished=0; n_draws=0.; n_losses = 0.
            times = []
            file_name = "models/trained_soft_generation"+str(gen)+".h5"
            ai1 = AI(mode="NN", size =10, player=1, load=True, model_file=file_name, random=True)
            print("\n Playing against stochastic generation %i" %gen)
            for i in range(max(100, int(n_games/(n_generation+1)))):
                t = time.time()
                winner = self.run_game(size=10, players=[ai1, ai2])
                n_finished+=1
                if winner==1:
                    n_wins+=1
                elif winner==0:
                    n_draws+=1
                else:
                    n_losses+=1
                if i%10==9:
                    times.append(time.time()-t)
                    mean_score = n_wins/(n_wins+n_losses)
                    sigma=0.5
                    Sn = np.sqrt(n_wins+n_losses) * (np.abs(mean_score-0.5))/(sigma)
                    gauss = norm()
                    p = 2*(1-norm.cdf(Sn))

                    minutes, sec = convert_time(np.mean(times[-10:])*(n_games-i)/10*len(times[-10:]))
                    sys.stdout.write("\r Current score after %i games : %i/%i/%i, p value : %.3f, ETA : %i min %i s" % (n_finished, n_wins, n_draws, n_losses, p, minutes, sec))

        self.positions = np.array(self.positions).reshape(len(self.positions), size, size, 1)
        self.scores = np.array(self.scores)
        self.positions, self.scores = get_symmetrical_positions(self.positions, self.scores)

        self.model= load_model(self.model_file)
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
        for self.gen in range(n_generation):
            self.gamma=min(0.5, ((self.gen+1)/(self.gen+2))**4)
            self.positions = []
            self.scores = []
            save_model_path = "models/trained_soft_generation%i.h5"%(self.gen)
            print("Generation %i training..."%(self.gen))
            self.run_generation(n_games=n_games, size=size, display=display, save_model_path=save_model_path, n_generation=self.gen)
            self.model_file = save_model_path
            # print("Generation %i testing vs random..."%(gen))
            # self.test_model_vs_random(n_games=30, size=10, display=False, model_path=self.model_file)




if __name__ == "__main__":
    ai = AI(load=False)
    T = Trainer(model_file="models/my_model.h5")
    T.run(n_generation=300)

    # ai1 = AI(mode="NN", size =10, player=1, load=True, model_file="models/trained_soft_generation7.h5")
    # game = Game(10, auto=False, display=True, training=False, players=["human", ai1])
    # game.run()


    # T.test_model_vs_random(model_path="models/trained.h5")
    pass
