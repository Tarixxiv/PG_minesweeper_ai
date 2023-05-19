import random
import numpy as np
from MineSweeper import MineSweeper


class QLearningAgent:
    def __init__(self, dimensions):
        self.game = MineSweeper(dimensions)
        self.qtable = {}

        self.agent_loop()

    def agent_loop(self):
        while self.game.game_result == 'safe':
            self.do_random_move()
        print("ended due to " + self.game.game_result)

    def do_random_move(self):
        y, x = random.choice(self.game.get_all_possible_moves())
        self.game.action(y, x)
        self.handle_qtable(y, x)

    def handle_qtable(self, y, x):
        neighbours = self.neighbours_to_string(self.game.get_neighbour_fields(y, x))

        if neighbours not in self.qtable:
            self.qtable[neighbours] = 0
        else:
            self.qtable += 1        #reward

    def neighbours_to_string(self, neighbours):
        neighbours = list(np.concatenate(neighbours).flat)
        string = ''.join(['B' if point == 'OoB' else str(point) for point in neighbours])
        return string
