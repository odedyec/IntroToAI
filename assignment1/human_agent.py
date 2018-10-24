from agent import BaseAgent
from simulator import HurricaneSimulator

class Human(BaseAgent):

    def choose_next_option(self, sim=HurricaneSimulator()):
        print('You are at: ', sim.state)
        next_state = input("Choose next step:")
        return int(next_state)