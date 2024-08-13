from G2048 import Game
import os
import pickle
import neat
import random
from math import log2
import warnings
import graphviz
import matplotlib.pyplot as plt
import numpy as np
import visualize
class Game_2048:
    def __init__(self, nplenes,seed):
        self.game=Game(nplenes,seed)
        self.board = self.game.board

    def test_ai(self, genome, config):
        net= neat.nn.FeedForwardNetwork.create(genome,config)
        run = True
        nmoved = 0
        while run: 
            moved=True
            self.game.display()
            in_neurons = self.normalize([j for i in self.board for j in i])
            output = net.activate(in_neurons)
            output_moves =  [(i, output[i]) for i in range(len(output))]
            output_moves = sorted(output_moves, key=lambda x: x[1])
            for (decision, weight) in output_moves:
                if decision == 0:
                    moved=self.game.slide_up()
                elif decision == 1:
                    moved=self.game.slide_down()
                elif decision == 2:
                    moved=self.game.slide_left()
                else:
                    moved=self.game.slide_right()
                
                if  moved:
                    self.game.add_new_tile()
                    break
            if not moved: nmoved = nmoved +1


            if self.game.game_over() or nmoved == 10: 
                break 
            
    def normalize(self,arr):
        val = max(arr)
        log_val = log2(val)
        if log_val == 0:
            return
        for i in range(len(arr)):
            if arr[i] != 0:
                arr[i] = log2(arr[i]) / log_val

        return arr            
          
    def train_ai(self, genome,config):
        run=True
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nmoved=0
        while run: 
            
            in_neurons = self.normalize([j for i in self.board for j in i])
            output = net.activate(in_neurons)
            #pillar si ha mogut o no si 10 cops fa moviment no valid para partida
            output_moves =  [(i, output[i]) for i in range(len(output))]
            output_moves = sorted(output_moves, key=lambda x: x[1])
            moved = True
            for (decision, weight) in output_moves:
                if decision == 0:
                    moved=self.game.slide_up()
                elif decision == 1:
                    moved=self.game.slide_down()
                elif decision == 2:
                    moved=self.game.slide_left()
                else:
                    moved=self.game.slide_right()
                
                if  moved:
                    self.game.add_new_tile()
                    break
                
            if not moved: nmoved = nmoved +1


            if self.game.game_over() or nmoved == 10: 
                game_info = (self.game.score, moved)
                self.calculate_fitness(genome, game_info)
                self.game.score=0
                run=False
                break
            


    
    def calculate_fitness(self, genome, game_info):
        score, moved= game_info
        smoothness = self.game.calc_smoothness()
        genome.fitness= (score / smoothness)* log2(self.board.max()) * -1
            


def eval_genomes(genomes, config):
    n= 1
    for i, (genome_id1, genome) in enumerate(genomes):
        genome.fitness= 0.0
        game = Game_2048(2,19)
        game.train_ai(genome, config)
        genome.fitness= genome.fitness
    


def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-169')
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10))
    winner=p.run(eval_genomes,50)
    visualize.draw_net(config, winner, True)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

def test_ai(config):
    with open("best.pickle", "rb") as f:
       winner = pickle.load(f)

    game = Game_2048(2,19)
    game.test_ai(winner,config)

if __name__== "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config= neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
 
    run_neat(config)
    #test_ai(config)
