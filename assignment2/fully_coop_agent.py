from game_tree_agent import GameTreeAgent
from simulator import HurricaneSimulator
from utils import *


class FullyCoopAgent(GameTreeAgent):

    def __init__(self, state):
        GameTreeAgent.__init__(self, state)

    def is_new_action_better(self, best_value, new_value, sim_emulator=HurricaneSimulator()):

        """
        Note that this function is called after apply_action is performed, so the player index
        is switched. Thus, we use "sim_emulator.agent_index - 1" to refer to the right player.
        """
        return sum(new_value) > sum(best_value)
