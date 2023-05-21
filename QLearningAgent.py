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
        self.random_flag_chance = 0.05
        self.win_count = 0
        self.loss_count = 0
        self.learning_rate = 0.9
        self.gamma = 0.99       #maybe bigger
        self.random_flag_chance_decay = 0.001       # random??
        self.random_move_chance_decay = 0.001
        self.previous_neighbours = None
        self.total_reward_in_episode = 0
        self.learn_and_test(dimensions)

    def agent_loop(self, dimensions):
        for episode in range(self.episodes):
            self.game = MineSweeper(dimensions)
            self.total_reward_in_episode = 0
            while self.game.game_result == 'safe':

                if random.random() > self.random_move_chance:
                    self.do_qtable_move()
                else:
                    self.do_random_move()

                self.random_move_chance = np.exp(-self.random_move_chance_decay*episode)    #maybe linear


            print("ended due to " + self.game.game_result)
            if self.game.game_result == "victory":
                self.add_non_revealed_mines_to_qtable()

            self.update_win_loss_count()
            print("wins :", self.win_count, ",losses :", self.loss_count,
                  ",win-loss ratio :", self.get_win_loss_ratio())

        print(sorted(((v, k) for k, v in self.qtable.items()), reverse=True))

    def add_non_revealed_mines_to_qtable(self):
        possible_moves = self.game.get_all_possible_moves()
        if possible_moves:
            for move in self.game.get_all_possible_moves():
                neighbours = self.game.get_neighbour_fields(*move)
                self.handle_qtable(neighbours, True)

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



    def do_random_move(self):
        y, x = random.choice(self.game.get_all_possible_moves())
        flag = random.random() <= self.random_flag_chance
        neighbours = self.game.get_neighbour_fields(y, x)
        if flag:
            self.game.flag(y, x)
        else:
            self.game.action(y, x)
        self.handle_qtable(neighbours, flag)

    def do_qtable_move(self):
        [y, x], flag = self.pick_best_qtable_move()
        neighbours = self.game.get_neighbour_fields(y, x)
        if flag:
            self.game.flag(y, x)
        else:
            self.game.action(y, x)
        self.handle_qtable(neighbours, flag)

    def pick_best_qtable_move(self):
        possible_moves = self.game.get_all_possible_moves()
        move_scores = []
        for move in possible_moves:
            neighbours = self.neighbours_to_string(self.game.get_neighbour_fields(*move))
            if neighbours in self.qtable:
                move_scores.append(self.qtable[neighbours])
            else:
                move_scores.append(0)

        #TODO flagi powinny być określane na bazie QTable a nie bo tak wychodzi, że abs się nada

        flag = False
        if max(move_scores) >= abs(min(move_scores)):
            best_move_indexes = [i for i in range(len(move_scores)) if move_scores[i] == max(move_scores)]
        else:
            flag = True
            best_move_indexes = [i for i in range(len(move_scores)) if move_scores[i] == min(move_scores)]

        return possible_moves[random.choice(best_move_indexes)], flag

    def handle_qtable(self, neighbours, flag):
        new_neighbours = self.neighbours_to_string(neighbours)
        neighbours = self.neighbours_to_string(neighbours)
        if neighbours not in self.qtable:
            self.qtable[neighbours] = 0

        contains_revealed_field = any(char.isdigit() for char in neighbours)
        if contains_revealed_field:
            if flag:
                #self.qtable[neighbours] -= self.game_result_to_reward(neighbours)
                reward = self.game_result_to_reward(neighbours)
            else:
                reward = self.game_result_to_reward(neighbours)
            self.qtable[neighbours] = self.learning_rate * self.qtable[neighbours] + self.learning_rate*(reward + self.gamma * self.qtable[new_neighbours])


    def game_result_to_reward(self, neighbours):
        #TODO nagroda za zwyciestwo dla wszzystkich ruchów
        #TODO Ponadto, każdy ruch ma być coraz mniej warty, zgodnie ze wzorem. Czy ma to też uwzględniać punktacje za zwyciestwonon?
        if self.game.game_result == "boom":
            return -1
        else:
            return 5

    def neighbours_to_string(self, neighbours):
        neighbours = list(np.concatenate(neighbours).flat)
        string = ''.join(['B' if point == 'OoB' else str(point) for point in neighbours])
        return string