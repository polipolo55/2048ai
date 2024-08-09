import numpy as np
import random

class Game:
  def __init__(self):
    self.board = np.zeros((4,4), dtype=int)
    self.score = 0
    self.GameOver = False
    self.add_new_tile()
    self.add_new_tile()
    self.nmovements=0
    
  def add_new_tile(self):
    empty_cells = list(zip(*np.where(self.board == 0)))
    if  empty_cells: 
      row, col = random.choice(empty_cells)
      self.board[row, col] = random.choices([2, 4], weights=[90, 10])[0]    

  def display(self):
    print(self.board)
    print(self.score)
    
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
            self.nmovements+=1
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
    

'''
def main():
  game = Game()
  game.display()
  command_mapping = {
    'w': game.slide_up,
    'a': game.slide_left,
    's': game.slide_down,
    'd': game.slide_right
  }

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

  
  