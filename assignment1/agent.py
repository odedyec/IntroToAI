from simulator import HurricaneSimulator


class BaseAgent:
    def __init__(self, state):
        self.path = []
        self.state = state
        self.full_state = None
        self.path.append(state)
        self.people_in_vehicle = 0
        self.should_pick_and_drop = True
        self.steps_explored = 0

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.path.append(new_state)
        self.state = new_state

    def check_if_path_ready(self, sim=HurricaneSimulator()):
        if len(self.path) == 0:
            return -1
        next_op = self.path.pop()
        if sim.graph[sim.get_state()][next_op].weight == -1:
            return -1
        return next_op

    def choose_next_option(self, sim=HurricaneSimulator()):
        raise NotImplementedError("")