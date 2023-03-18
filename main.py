import random


def insert_mine(board, y, x):
    board[y][x] = '*'
    for y_offset in range(-1, 2):
        for x_offset in range(-1, 2):
            try:
                if board[y + y_offset][x + x_offset] != '*' and y + y_offset >= 0 and x + x_offset >= 0:
                    board[y + y_offset][x + x_offset] += 1
            except IndexError:
                print(y + y_offset, x + x_offset)
                pass


def print_full_board(board):
    dimensions = len(board)
    for i in range(dimensions):
        row = ""
        for j in range(dimensions):
            row += str(board[i][j])
        print(row)


def print_player_map(board, fog_of_war_map):
    dimensions = len(board)
    for i in range(dimensions):
        row = ""
        for j in range(dimensions):
            if fog_of_war_map[i][j]:
                row += str(board[i][j])
            else:
                row += "#"
        print(row)


def generate_fog_of_war_map(dimensions):
    output = []
    for i in range(dimensions):
        row = []
        for j in range(dimensions):
            row.append(0)
        output.append(row)
    return output


def place_mines(board, mine_count):
    dimensions = len(board)

    mines = random.sample(range(0, dimensions ** 2), mine_count)
    mines.sort()
    mines = [[x // dimensions, x % dimensions] for x in mines]

    for mine in mines:
        insert_mine(board, mine[0], mine[1])


def generate_board(dimensions):
    output = []
    for i in range(dimensions):
        row = []
        for j in range(dimensions):
            row.append(0)
        output.append(row)

    return output


def reveal(y, x, board, fog_of_war_map, move_count):
    try:
        move_count[0] += 1
        fog_of_war_map[y][x] = 1
        if board[y][x] == '*':
            print("boom!!!")
            print_full_board(board)
            return "boom"
        elif board[y][x] == 0:
            for y_offset in range(-1, 2):
                for x_offset in range(-1, 2):
                    try:
                        if y + y_offset >= 0 and x + x_offset >= 0 and fog_of_war_map[y + y_offset][x + x_offset] != 1:
                            reveal(y + y_offset, x + x_offset, board, fog_of_war_map, move_count)
                    except IndexError:
                        pass
    except IndexError:
        pass

    return "safe"


def play(dimensions):
    board = generate_board(dimensions)
    fog_of_war_map = generate_fog_of_war_map(dimensions)
    random.seed()
    mine_count = random.randint(len(board) ** 2 // 8, len(board) ** 2 // 4)
    place_mines(board, mine_count)
    print_player_map(board, fog_of_war_map)
    print_full_board(board)
    gamestate = "safe"
    move_count = [0]
    while gamestate == "safe":
        print_player_map(board, fog_of_war_map)
        y, x = map(int, input().split())                #ten input podmienimy na input dla SI
        gamestate = reveal(y, x, board, fog_of_war_map, move_count)
        if gamestate != "boom" and move_count[0] + mine_count == dimensions ** 2:
            gamestate = "victory"
            print("Mission accomplished")


if __name__ == '__main__':
    play(10)
