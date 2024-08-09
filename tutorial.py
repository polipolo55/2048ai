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

            if moved: 
                self.game.add_new_tile()
            if self.game.game_over(): 
                break 
            self.game.display()

    def train_ai(self, genome,config):
        run = True
        notMoved = 0
        net = neat.nn.FeedForwardNetwork.create(genome,config)
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
            if not moved: notMoved+=1
            else: 
                self.game.add_new_tile()
            game_info = (self.game.score, self.game.nmovements, notMoved)
            if self.game.game_over(): 
                self.calculate_fitness(genome, game_info)
                run=False
                break
            
            
    
    def calculate_fitness(self, genome, game_info):
        score, nmovements, notMoved = game_info
        
        max_tile = self.board.max()
        
        fitness = float(score)
        
        fitness += max_tile ** 2
        
        fitness -= nmovements * 0.1
        
        fitness -= notMoved * 2
        
        stability_bonus = 0
        for x in range(4):
            for y in range(4):
                if x < 3:
                    stability_bonus -= abs(self.board[x, y] - self.board[x+1, y])
                if y < 3:
                    stability_bonus -= abs(self.board[x, y] - self.board[x, y+1])
        
        fitness += stability_bonus * 0.1
        
        genome.fitness += fitness
            
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
