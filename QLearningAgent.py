import random
import numpy as np
from MineSweeper import MineSweeper


class QLearningAgent:
    def __init__(self, dimensions, random_move_chance, random_move_chance_test):
        self.game = None
        self.qtable = {}
        self.episodes = 50000
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
            return self.win_count / (self.win_count + self.loss_count)
        else:
            return 0

    def game_result_to_reward(self):
        if self.game.game_result == "safe":
            return 1
        else:
            return -5

    def do_random_move(self):
        y, x = random.choice(self.game.get_all_possible_moves())
        neighbours = self.game.get_neighbour_fields(y, x)
        self.game.action(y, x)
        self.handle_qtable(neighbours)

    def pick_best_qtable_move(self):
        possible_moves = self.game.get_all_possible_moves()
        move_scores = []
        for move in possible_moves:
            neighbours = self.neighbours_to_string(self.game.get_neighbour_fields(*move))
            if neighbours in self.qtable:
                move_scores.append(self.qtable[neighbours])
            else:
                move_scores.append(0)

        best_move_indexes = [i for i in range(len(move_scores)) if move_scores[i] == max(move_scores)]
        return possible_moves[random.choice(best_move_indexes)]

    def do_qtable_move(self):
        y, x = self.pick_best_qtable_move()
        neighbours = self.game.get_neighbour_fields(y, x)
        self.game.action(y, x)
        self.handle_qtable(neighbours)

    def handle_qtable(self, neighbours):
        #neighbours = self.neighbours_to_string(neighbours)

        neighbours = self.sum_neighbours(neighbours)
        if neighbours not in self.qtable:
            self.qtable[neighbours] = 0

#        contains_revealed_field = any(char.isdigit() for char in neighbours)
        contains_revealed_field = neighbours
        if contains_revealed_field:
            self.qtable[neighbours] += self.game_result_to_reward()

    def neighbours_to_string(self, neighbours):
        neighbours = list(np.concatenate(neighbours).flat)
        string = ''.join(['B' if point == 'OoB' else str(point) for point in neighbours])
        return string

    def sum_neighbours(self, neighbours):
        neighbours = list(np.concatenate(neighbours).flat)
        sum = 0
        for point in neighbours:
            if point != 'OoB' and point != '#':
                sum += int(point)

        return sum