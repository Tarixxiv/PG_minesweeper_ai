from QLearningAgent import QLearningAgent
from MineSweeper import MineSweeper

if __name__ == '__main__':
    q = QLearningAgent()
    q.agent_loop(5, 5000)

