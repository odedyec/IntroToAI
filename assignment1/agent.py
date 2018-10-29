from simulator import HurricaneSimulator


class BaseAgent:
    def __init__(self, state):
        self.path = []
        self.state = state
        self.path.append(state)
        self.people_in_vehicle = 0

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.path.append(new_state)
        self.state = new_state

    def choose_next_option(self, sim=HurricaneSimulator()):
        raise NotImplementedError("")