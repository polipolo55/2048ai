import numpy as np
import random
import keyboard

class Game:
    def __init__(self):
        self.board = np.zeros((4, 4), dtype=int)
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = list(zip(*np.where(self.board == 0)))
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row, col] = 2

    def display(self):
        print(self.board)

    def slide_left(self):
        moved = False
        for row in range(4):
            new_row = self.board[row, self.board[row] != 0]
            new_row = np.pad(new_row, (0, 4 - len(new_row)), 'constant')
        for col in range(3):
            if new_row[col] == new_row[col + 1] and new_row[col] != 0:
                new_row[col] *= 2
                new_row[col + 1:] = np.roll(new_row[col + 1:], -1)
                new_row[col + 1] = 0
                moved = True
        if not np.array_equal(self.board[row], new_row):
            moved = True
            self.board[row] = new_row
        return moved

    def slide_right(self):
        self.board = np.fliplr(self.board)
        moved = self.slide_left()
        self.board = np.fliplr(self.board)
        return moved

    def slide_up(self):
        self.board = np.rot90(self.board, -1)
        moved = self.slide_left()
        self.board = np.rot90(self.board)
        return moved

    def slide_down(self):
        self.board = np.rot90(self.board)
        moved = self.slide_left()
        self.board = np.rot90(self.board, -1)
        return moved

def main():
    game = Game()
    game.display()

    def handle_input(event):
        if event.name == 'left':
            if game.slide_left():
                game.add_new_tile()
        elif event.name == 'right':
            if game.slide_right():
                game.add_new_tile()
        elif event.name == 'up':
            if game.slide_up():
                game.add_new_tile()
        elif event.name == 'down':
            if game.slide_down():
                game.add_new_tile()
        game.display()

    keyboard.on_press(handle_input)

    print("Use arrow keys to play the game. Press 'esc' to exit.")
    keyboard.wait('esc')

if __name__ == "__main__":
    main()