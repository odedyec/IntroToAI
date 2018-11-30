from agent import BaseAgent
from simulator import HurricaneSimulator
from shortest_path import dijkstra_shortest_path

inf = 2 ** 31

class Vandal(BaseAgent):

    def __init__(self, state):
        super(Vandal, self).__init__(state)
        self.turn_to_wait = -1
        self.should_pick_and_drop = False

    def find_lowest(self, sim=HurricaneSimulator()):
        weight_grid = sim.get_weights()
        lowest_cost = (-1, inf)
        for i in range(sim.num_of_vertices):
            if 0 < weight_grid[self.state][i] < lowest_cost[1]:
                lowest_cost = (weight_grid[self.state][i], i)
        return lowest_cost

    def choose_next_option(self, sim=HurricaneSimulator()):
        self.set_state(sim.get_state())

        if self.turn_to_wait > 1:
            self.turn_to_wait -= 1
            return -1

        elif self.turn_to_wait == 1:
            lowest_cost = self.find_lowest(sim)
            if lowest_cost[1] != inf:
                # block
                sim.graph[self.state][lowest_cost[1]].weight = -1
                sim.graph[lowest_cost[1]][self.state].weight = -1
            self.turn_to_wait -= 1
            return -1

        elif self.turn_to_wait == 0:
            lowest_cost = self.find_lowest(sim)
            if lowest_cost[1] != inf:
                return lowest_cost[1]
            else:
                return -1

        elif self.turn_to_wait < 0:
            self.turn_to_wait = self.state
            return -1

