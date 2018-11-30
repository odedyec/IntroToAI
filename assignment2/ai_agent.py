from smart_greedy_agent import SmartGreedy
from simulator import HurricaneSimulator


class AIAgent(SmartGreedy):

    def choose_next_option(self, sim=HurricaneSimulator()):
        return -1