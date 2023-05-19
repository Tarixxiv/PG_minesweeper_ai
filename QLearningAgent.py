import random
import numpy as np
from MineSweeper import MineSweeper


class QLearningAgent:
    def __init__(self, dimensions):
        self.game = None
        self.qtable = {}
        self.episodes = 1000
        self.random_move_chance = 0.01
        self.agent_loop(dimensions)
        print(self.qtable)

    def agent_loop(self, dimensions):
        for episode in range(self.episodes):
            self.game = MineSweeper(dimensions)
            while self.game.game_result == 'safe':
                if random.random() > self.random_move_chance:
                    self.do_qtable_move()
                else:
                    self.do_random_move()

            print("ended due to " + self.game.game_result)

    def game_result_to_reward(self):
        if self.game.game_result == "safe":
            return 1
        else:
            return -1

    def do_random_move(self):
        y, x = random.choice(self.game.get_all_possible_moves())
        self.game.action(y, x)
        self.handle_qtable(y, x)

    def do_qtable_move(self):
        possible_moves = self.game.get_all_possible_moves()
        move_scores = []
        for move in possible_moves:
            neighbours = self.neighbours_to_string(self.game.get_neighbour_fields(*move))
            if neighbours in self.qtable:
                move_scores.append(self.qtable[neighbours])
            else:
                move_scores.append(0)
        best_move_index = move_scores.index(max(move_scores))
        y, x = possible_moves[best_move_index]
        self.game.action(y, x)
        self.handle_qtable(y, x)

    def handle_qtable(self, y, x):
        neighbours = self.neighbours_to_string(self.game.get_neighbour_fields(y, x))
        if neighbours not in self.qtable:
            self.qtable[neighbours] = 0
        else:
            self.qtable[neighbours] += self.game_result_to_reward()

    def neighbours_to_string(self, neighbours):
        neighbours = list(np.concatenate(neighbours).flat)
        string = ''.join(['B' if point == 'OoB' else str(point) for point in neighbours])
        return string
