import random

from MineSweeper import MineSweeper


class QLearningAgent:
    def __init__(self, dimensions):
        self.game = MineSweeper(dimensions)
        self.qtable = []

        self.agent_loop()

    def agent_loop(self):
        while self.game.game_result == 'safe':
            self.do_random_move()
        print("ended due to " + self.game.game_result)

    def do_random_move(self):
        y, x = random.choice(self.game.get_all_possible_moves())
        self.game.action(y, x) #move[0], move[1])
        self.handle_qtable(y, x) #move[0], move[1])

    def handle_qtable(self, y, x):
        print("neighbours: ")
        neighbours = self.game.get_neighbour_fields(y, x)
        print(neighbours)
        if neighbours not in self.qtable:
            self.qtable.append(neighbours)

    def neighbours_to_string(self, list):

        for point in list:
            if point == 'OoB':



