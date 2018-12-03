from game_tree_agent import GameTreeAgent
from greedy_agent import Greedy
from simulator import HurricaneSimulator
from utils import *
from math import isinf, inf


class AdverserialAgent(GameTreeAgent):

    def __init__(self, state):
        GameTreeAgent.__init__(self, state)
        self.is_zero_sum = True

    @staticmethod
    def is_new_action_better(best_value, new_value, sim_emulator=HurricaneSimulator()):
        """
        Note that this function is called after apply_action is performed, so the player index
        is switched. Thus, we use "sim_emulator.agent_index - 1" to refer to the right player.
        """
        cur_best = best_value[1 - sim_emulator.agent_index] - best_value[sim_emulator.agent_index]
        if isinf(best_value[sim_emulator.agent_index]) and best_value[sim_emulator.agent_index] < 0:
            '" If the second score is - infinity, set the subtraction to be - infinity "'
            cur_best = -inf

        return new_value[1 - sim_emulator.agent_index] - new_value[sim_emulator.agent_index] >= cur_best

    @staticmethod
    def get_max_agent_score(value_tuple):
        return value_tuple[0] - value_tuple[1]
