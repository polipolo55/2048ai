import numpy as np
import math
from math import log2
class Game:
  def __init__(self, nplenes, seed):
    self.board = np.zeros((4,4), dtype=int)
    self.score = 0
    self.GameOver = False
    np.random.seed(seed)
    for i in range(nplenes):
      self.add_new_tile()
    self.nmovements=0
    
  def add_new_tile(self):
    empty_cells = list(zip(*np.where(self.board == 0)))
    if  empty_cells: 
      np.random.shuffle(empty_cells)
      row, col = empty_cells[0]
      self.board[row, col] = np.random.choice([2, 4], p=[0.8, 0.2])

  def display(self):
    print(self.board)
    print(self.score)

  def calc_smoothness(self):
    board=self.board
    smoothness = 0
    for rotation in range(2):
      for i in range(0, len(board)):
          for j in range(0, len(board[i])):
              if board[i][j] != 0 and j + 1 < len(board[i]) and board[i][j + 1] != 0:
                current_smoothness = math.fabs(log2(board[i][j]) - log2(board[i][j + 1]))
                smoothness = smoothness - current_smoothness
      np.rot90(board)
  
    return smoothness
  
  def slide_left(self):
      moved = False
      for row in range(4):
        new_row = self.board[row, self.board[row] != 0]
        new_row = np.pad(new_row, (0, 4 - len(new_row)), 'constant')
        for col in range(3):
          if new_row[col] == new_row[col + 1] and new_row[col] != 0:
            new_row[col] *= 2
            self.score += new_row[col]
            new_row[col + 1] = 0
            moved = True
        new_row = new_row[new_row != 0]
        new_row = np.pad(new_row, (0, 4 - len(new_row)), 'constant')
        
        if not np.array_equal(self.board[row], new_row):
            moved = True
            self.nmovements+=1
            self.board[row] = new_row
      return moved

  def slide_right(self):
    self.board = np.fliplr(self.board)
    moved = self.slide_left()
    self.board = np.fliplr(self.board)
    return moved

  def slide_down(self):
    self.board = np.rot90(self.board, -1)
    moved = self.slide_left()
    self.board = np.rot90(self.board)
    return moved

  def slide_up(self):
    self.board = np.rot90(self.board)
    moved = self.slide_left()
    self.board = np.rot90(self.board, -1)
    return moved

  def game_over(self):
    temp_board = self.board.copy()
    temp_score = self.score
    temp_nmovements = self.nmovements
    moved = True
    if self.slide_left() or self.slide_right() or self.slide_up() or self.slide_down():
      moved = False
    
    self.board = temp_board
    self.score = temp_score
    self.nmovements = temp_nmovements
    return moved

  def fusion_move(self):
  
    for i in self.board:
      new_row=i[i != 0]
      if(len(new_row) > 1):
        for j in range(len(new_row)-1):
          if new_row[j] == new_row[j+1]:
            return True
  
    for i in range(4):
      new_col = self.board[:,i]
      new_col = new_col[new_col != 0]
      if len(new_col)>1:
        for j in range(len(new_col)-1):
          if new_col[j] == new_col[j+1]:
            return True
    
    return False

'''
def main():
  game = Game(2)
  command_mapping = {
    'w': game.slide_up,
    'a': game.slide_left,
    's': game.slide_down,
    'd': game.slide_right
  }
  game.display()
  print(game.fusion_move())
  while True:
      command = input("Enter command (w/a/s/d): ").strip().lower()
      if command in command_mapping:
          moved = command_mapping[command]()
          if moved:
            game.add_new_tile()
            if game.game_over():
              game.GameOver = True
              print("Game over!")
              break
          game.display()
      else:
          print("Invalid command. Use 'w', 'a', 's', or 'd'.")

if __name__ == "__main__":
    main()

'''

  
  