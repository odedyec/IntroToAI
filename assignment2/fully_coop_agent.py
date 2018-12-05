from game_tree_agent import GameTreeAgent
from simulator import HurricaneSimulator
from utils import *


class FullyCoopAgent(GameTreeAgent):

    def __init__(self, state):
        GameTreeAgent.__init__(self, state)

    def is_new_action_better(self, best_value, new_value, sim_emulator=HurricaneSimulator()):

        """
        A fully cooperative both agents aim to maximize the sum of scores.
        """
        return sum(new_value) > sum(best_value)
