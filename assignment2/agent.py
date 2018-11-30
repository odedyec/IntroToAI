

class BaseAgent:
    def __init__(self, state):
        self.path = []
        self.state = state
        self.full_state = None
        # self.path.append(state)
        self.people_in_vehicle = 0
        self.people_saved = 0
        self.should_pick_and_drop = True
        self.expanded_nodes = 0

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        # self.path.append(new_state)
        self.state = new_state

    def add_people_to_vehicle(self, num_of_people):
        self.people_in_vehicle += num_of_people

    def reached_shelter(self):
        self.people_saved += self.people_in_vehicle
        self.people_in_vehicle = 0

    def check_if_path_ready(self, sim):
        if len(self.path) == 0:
            return -1
        next_op = self.path.pop(0)['state']
        if sim.graph[sim.get_state()][next_op].weight == -1:
            return -1
        return next_op

    def choose_next_option(self, sim):
        raise NotImplementedError("")