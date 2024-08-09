from G2048 import Game
import os
import pickle
import neat

class Game_2048:
    def __init__(self):
        self.game=Game()
        self.board = self.game.board

    def test_ai(self, genome, config):
        net= neat.nn.FeedForwardNetwork.create(genome,config)
        nlock=0
        run = True
        while run: 

            b = self.board.flatten()
            output = net.activate(b)
            #pillar si ha mogut o no si 10 cops fa moviment no valid para partida
            decision = output.index(max(output))
            moved = True
            if decision == 0:
                moved=self.game.slide_up()
            elif decision == 1:
                moved=self.game.slide_down()
            elif decision == 2:
                moved=self.game.slide_left()
            else:
                moved=self.game.slide_right()

            if not moved: nlock+=1
            else: 
                nlock=0
                self.game.add_new_tile()
            game_info = (self.game.score, nlock, self.game.nmovements)
            if nlock == 2 or self.game.game_over(): 
                break 
            self.game.display()

    def train_ai(self, genome,config):
        run=True
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nlock=0
        while run: 
            self.game.display()
            b = self.board.flatten()
            output = net.activate(b)
            #pillar si ha mogut o no si 10 cops fa moviment no valid para partida
            decision = output.index(max(output))
            moved = True
            if decision == 0:
                moved=self.game.slide_up()
            elif decision == 1:
                moved=self.game.slide_down()
            elif decision == 2:
                moved=self.game.slide_left()
            else:
                moved=self.game.slide_right()
            if not moved: nlock+=1
            else: 
                nlock=0
                self.game.add_new_tile()
            game_info = (self.game.score, self.game.nmovements)
            if nlock == 2 or self.game.game_over(): 
                self.calculate_fitness(genome, game_info)
                run=False
                break
            
            
    
    def calculate_fitness(self, genome, game_info):
        genome.fitness += float(game_info[0]) + float(game_info[1]) 
            

def eval_genomes(genomes, config):
    for i, (genome_id1, genome) in enumerate(genomes):
        genome.fitness= 0.0
        game = Game_2048()
        game.train_ai(genome, config)


def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(15))

    winner= p.run(eval_genomes, 300)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

def test_ai(config):
    with open("best.pickle", "rb") as f:
       winner = pickle.load(f)

    game = Game_2048()
    game.test_ai(winner)

if __name__== "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config= neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    run_neat(config)
