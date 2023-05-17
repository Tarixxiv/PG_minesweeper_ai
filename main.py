import random


class MineSweeper:
    def __init__(self, dimensions):
        self.board = []
        self.fog_of_war_map = []
        self.move_count = 0
        self.mine_count = 0
        self.dimensions = dimensions
        self.game_result = "safe"

    def insert_mine(self, y, x):
        self.board[y][x] = '*'
        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                try:
                    if self.board[y + y_offset][x + x_offset] != '*' and y + y_offset >= 0 and x + x_offset >= 0:
                        self.board[y + y_offset][x + x_offset] += 1
                except IndexError:
                    print(y + y_offset, x + x_offset)
                    pass

    def print_full_board(self):
        dimensions = len(self.board)
        for i in range(dimensions):
            row = ""
            for j in range(dimensions):
                row += str(self.board[i][j])
            print(row)

        print()

    def print_player_map(self):
        dimensions = len(self.board)
        for i in range(dimensions):
            row = ""
            for j in range(dimensions):
                if self.fog_of_war_map[i][j]:
                    row += str(self.board[i][j])
                else:
                    row += "#"
            print(row)

        print()

    def generate_fog_of_war_map(self):
        output = []
        for i in range(self.dimensions):
            row = []
            for j in range(self.dimensions):
                row.append(0)
            output.append(row)
        self.fog_of_war_map = output

    def place_mines(self):
        dimensions = len(self.board)

        mines = random.sample(range(0, dimensions ** 2), self.mine_count)
        mines.sort()
        mines = [[x // dimensions, x % dimensions] for x in mines]

        for mine in mines:
            self.insert_mine(mine[0], mine[1])

    def generate_board(self):
        output = []
        for i in range(self.dimensions):
            row = []
            for j in range(self.dimensions):
                row.append(0)
            output.append(row)
        self.board = output

    def reveal_adjacent(self, y, x):
        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                try:
                    if y + y_offset >= 0 and x + x_offset >= 0 and self.fog_of_war_map[y + y_offset][x + x_offset] != 1:
                        self.reveal(y + y_offset, x + x_offset)
                except IndexError:
                    pass

    def reveal(self, y, x):
        try:
            self.move_count += 1
            self.fog_of_war_map[y][x] = 1
            if self.board[y][x] == '*':
                print("boom!!!")
                self.print_full_board()
                self.game_result = "boom"
            if self.board[y][x] == 0:
                self.reveal_adjacent(y, x)
        except IndexError:
            pass

        return "safe"

    def checkWin(self):
        if self.game_result != "boom" and self.move_count + self.mine_count == self.dimensions ** 2:
            print("Mission accomplished")
            self.game_result = "victory"

    def play(self):
        self.generate_board()
        self.generate_fog_of_war_map()
        random.seed()
        self.mine_count = random.randint(self.dimensions ** 2 // 16, self.dimensions ** 2 // 8)
        # Only the mines on the board are strings, the rest are ints
        self.place_mines()
        self.print_full_board()
        game_state = "safe"
        while game_state == "safe":
            self.print_player_map()
            y, x = self.action()
            if self.fog_of_war_map[y][x] == 0:
                self.reveal(y, x)
                self.checkWin()

    def reset(self):
        self.generate_fog_of_war_map()
        self.move_count = 0

    def action(self):
        return map(int, input("wpisz rząd i kolumnę\n").split())


if __name__ == '__main__':
    a = MineSweeper(10)
    a.play()
