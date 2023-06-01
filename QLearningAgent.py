import random
import numpy as np
from MineSweeper import MineSweeper


class QLearningAgent:
    def __init__(self):
        self.game = None
        self.qtable = {}
        self.random_move_chance = 1
        self.min_random_move_chance = 0.01
        self.random_flag_chance = 0.5
        self.win_count = 0
        self.loss_count = 0
        self.learning_rate = 0.1
        self.random_flag_chance_decay = 0.05
        self.min_random_flag_chance = 0.005
        self.random_move_chance_decay = 0.001
        self.previous_neighbours = None
        self.total_reward_in_episode = 0
        self.move_types = {"default": 0, "flag": 1}

    def agent_loop(self, dimensions, episodes):
        win_ratio_history = []

        for episode in range(episodes):
            self.game = MineSweeper(dimensions)
            self.total_reward_in_episode = 0
            while self.game.game_result == 'safe':

                if random.random() > self.random_move_chance:
                    self.do_qtable_move()
                else:
                    self.do_random_move()

                self.random_move_chance = max(self.min_random_move_chance, np.exp(-self.random_move_chance_decay * episode))
                self.random_flag_chance = max(self.min_random_flag_chance, np.exp(-self.random_flag_chance_decay * episode))

          #  print("ended due to " + self.game.game_result)
            if self.game.game_result == "victory":
                self.add_non_revealed_mines_to_qtable()

            self.update_win_loss_count()
            print("episode: ", self.win_count + self.loss_count, ",wins :", self.win_count, ",losses :", self.loss_count,
                  ",win rate:", self.get_win_rate())
            win_ratio_history.append(self.get_win_rate())


        print(sorted(((v, k) for k, v in self.qtable.items()), reverse=True))
        return win_ratio_history


    def add_non_revealed_mines_to_qtable(self):
        possible_moves = self.game.get_all_possible_moves()
        if possible_moves:
            for move in self.game.get_all_possible_moves():
                neighbours = self.game.get_neighbour_fields(*move)
                self.handle_qtable(neighbours, self.move_types["flag"])

    def update_win_loss_count(self):
        if self.game.game_result == "boom":
            self.loss_count += 1
        else:
            self.win_count += 1

    def get_win_rate(self):
        if self.win_count + self.loss_count != 0:
            return self.win_count / (self.win_count + self.loss_count)
        else:
            return 0

    def do_random_move(self):
        y, x = random.choice(self.game.get_all_possible_moves())
        flag = random.random() <= self.random_flag_chance
        old_neighbours = self.game.get_neighbour_fields(y, x)
        if flag:
            self.game.flag(y, x)
            move_type = self.move_types["flag"]
        else:
            self.game.action(y, x)
            move_type = self.move_types["default"]
        self.handle_qtable(old_neighbours, move_type)

    def do_qtable_move(self):
        [y, x], flag = self.pick_best_qtable_move()
        old_neighbours = self.game.get_neighbour_fields(y, x)
        if flag:
            self.game.flag(y, x)
        else:
            self.game.action(y, x)
        self.handle_qtable(old_neighbours, flag)

    def pick_best_qtable_move(self):
        possible_moves = self.game.get_all_possible_moves()
        move_scores = []
        for move in possible_moves:
            neighbours = self.neighbours_to_string(self.game.get_neighbour_fields(*move))
            if neighbours in self.qtable:
                move_scores.append(max(self.qtable[neighbours]))
            else:
                move_scores.append(0)

        best_move_indexes = [i for i in range(len(move_scores)) if move_scores[i] == max(move_scores)]

        chosen_move = possible_moves[random.choice(best_move_indexes)]
        neighbours = self.neighbours_to_string(self.game.get_neighbour_fields(*chosen_move))
        if neighbours in self.qtable:
            move_type = self.qtable[neighbours].index(max(self.qtable[neighbours]))
        else:
            move_type = random.choice(list(self.move_types.values()))

        return chosen_move, move_type

    def handle_qtable(self, old_neighbours, move_type):
        old_neighbours = self.neighbours_to_string(old_neighbours)
        if old_neighbours not in self.qtable:
            self.qtable[old_neighbours] = [0] * len(self.move_types)

        contains_revealed_field = any(char.isdigit() for char in old_neighbours)
        if contains_revealed_field:
            reward = self.game_result_to_reward(move_type)
            self.qtable[old_neighbours][move_type] = (1-self.learning_rate) * self.qtable[old_neighbours][move_type] + self.learning_rate * reward

    def game_result_to_reward(self, move_type):
        if self.game.game_result == "boom":
            return -1
        elif move_type == 1:
            return 2
        else:
            return 1

    def neighbours_to_string(self, neighbours):
        neighbours = list(np.concatenate(neighbours).flat)
        string = ''.join(['B' if point == 'OoB' else str(point) for point in neighbours])
        return string
