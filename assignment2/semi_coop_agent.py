from game_tree_agent import GameTreeAgent
from simulator import HurricaneSimulator
from utils import *
from copy import deepcopy


class SemiCoopAgent(GameTreeAgent):

    def __init__(self, state):
        GameTreeAgent.__init__(self, state)

    def is_new_action_better(self, best_value, new_value, sim_emulator=HurricaneSimulator()):
        """ check, based on game type, if the new value is better than current best value """
        return (new_value[1 - sim_emulator.agent_index] > best_value[1 - sim_emulator.agent_index] or
                (new_value[1 - sim_emulator.agent_index] == best_value[1 - sim_emulator.agent_index] and
                new_value[sim_emulator.agent_index] > best_value[sim_emulator.agent_index]))
