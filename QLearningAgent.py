import random
import numpy as np
from MineSweeper import MineSweeper


class QLearningAgent:
    def __init__(self, dimensions, random_move_chance, random_move_chance_test):
        self.game = None
        self.qtable = {}
        self.episodes = 5000
        self.random_move_chance = random_move_chance
        self.random_move_chance_test = random_move_chance_test
        self.win_count = 0
        self.loss_count = 0
        self.learn_and_test(dimensions)

    def agent_loop(self, dimensions):
        for episode in range(self.episodes):
            self.game = MineSweeper(dimensions)
            while self.game.game_result == 'safe':
                if random.random() > self.random_move_chance:
                    self.do_qtable_move()
                else:
                    self.do_random_move()

            print("ended due to " + self.game.game_result)
            self.update_win_loss_count()
            print("wins :", self.win_count, ",losses :", self.loss_count,
                  ",win-loss ratio :", self.get_win_loss_ratio())

        print(sorted(((v, k) for k, v in self.qtable.items()), reverse=True))

    def learn_and_test(self, dimensions):
        self.agent_loop(dimensions)
        self.random_move_chance = self.random_move_chance_test
        self.win_count = 0
        self.loss_count = 0
        self.agent_loop(dimensions)



    def update_win_loss_count(self):
        if self.game.game_result == "boom":
            self.loss_count += 1
        else:
            self.win_count += 1

    def get_win_loss_ratio(self):
        if self.win_count + self.loss_count != 0:
            return self.win_count/(self.win_count + self.loss_count)
        else:
            return 0

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
            neighbours = self.neighbours_to_string(*move)
            if neighbours in self.qtable:
                move_scores.append(self.qtable[neighbours])
            else:
                move_scores.append(0)
        best_move_index = move_scores.index(max(move_scores))
        y, x = possible_moves[best_move_index]
        self.game.action(y, x)
        self.handle_qtable(y, x)

    def handle_qtable(self, y, x):
        neighbours = self.neighbours_to_string(y, x)
        if neighbours not in self.qtable:
            self.qtable[neighbours] = 0
        self.qtable[neighbours] += self.game_result_to_reward()

    def neighbours_to_string(self, y, x):
        neighbour_grid = self.game.get_neighbour_fields(y, x)
        neighbours = list(np.concatenate(neighbour_grid).flat)
        middle_field_index = int(len(neighbours)/2)
        neighbours[middle_field_index] = '#'
        string = ''.join(['B' if point == 'OoB' else str(point) for point in neighbours])
        return string
