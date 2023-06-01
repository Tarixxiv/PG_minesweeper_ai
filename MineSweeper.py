import random


class MineSweeper:
    def __init__(self, dimensions):
        self.board = []
        self.board_backup = []
        self.fog_of_war_map = []
        self.revealed_fields_count = 0
        self.mine_count = 0
        self.dimensions = dimensions

        self.game_result = "safe"
        self.new_game()

    def insert_mine(self, y, x):
        self.board[y][x] = '*'
        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                try:
                    if self.board[y + y_offset][x + x_offset] != '*' and y + y_offset >= 0 and x + x_offset >= 0:
                        self.board[y + y_offset][x + x_offset] += 1
                except IndexError:
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
        self.board_backup = self.board

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
            self.revealed_fields_count += 1
            self.fog_of_war_map[y][x] = 1
            if self.board[y][x] == '*':
                #print("boom!!!")
                #self.print_full_board()
                self.game_result = "boom"
            if self.board[y][x] == 0:
                self.reveal_adjacent(y, x)
        except IndexError:
            pass

        return "safe"

    def check_win(self):
        if self.game_result != "boom" and self.revealed_fields_count + self.mine_count == self.dimensions ** 2:
            #print("Mission accomplished")
            self.game_result = "victory"

    def action(self, y, x):
        # uncomment for manual control
        # y, x = self.manual_control()
        if self.fog_of_war_map[y][x] == 0:
            self.reveal(y, x)
            self.check_win()
        #self.print_player_map()
        # returns string : "safe"/"victory"/"boom"
        return self.game_result

    def flag(self, y, x):
        if self.fog_of_war_map[y][x] == 0:
            if self.board[y][x] == "*":
                self.board[y][x] = "F"
                #flags don't count torwards revealed fields
                self.revealed_fields_count -= 1
            else:
                #replaces safe field with bomb to cause loss
                self.board[y][x] = "*"
            self.action(y, x)



    def get_all_possible_moves(self):
        return [[y, x] for y in range(self.dimensions) for x in range(self.dimensions) if
                self.fog_of_war_map[y][x] == 0]

    def reset(self):
        self.board = self.board_backup
        self.generate_fog_of_war_map()
        self.revealed_fields_count = 0
        self.game_result = "safe"

    def new_game(self):
        self.reset()
        self.generate_board()
        self.mine_count = random.randint(self.dimensions ** 2 // 16, self.dimensions ** 2 // 8)
        # Only the mines on the board are strings, the rest are ints
        self.place_mines()
        #self.print_full_board()

    def get_neighbour_fields(self, y, x):
        output = []
        for yi in range(-1, 2):
            row = []
            for xi in range(-1, 2):
                if y + yi in range(0, self.dimensions) and x + xi in range(0, self.dimensions):
                    if self.fog_of_war_map[y + yi][x + xi]:
                        row.append(self.board[y + yi][x + xi])
                    else:
                        row.append("#")
                else:
                    row.append("OoB")
            output.append(row)
        return output

    def manual_control(self):
        return map(int, input("wpisz rząd i kolumnę\n").split())