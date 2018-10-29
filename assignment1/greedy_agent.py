from agent import BaseAgent
from simulator import HurricaneSimulator
from numpy import inf
from shortest_path import dijkstra_shortest_path


class Greedy(BaseAgent):

    def search_grid(self, grid, sim=HurricaneSimulator()):
        l_cost = []
        weight_grid = sim.get_weights()
        for i in range(sim.num_of_vertices):
            if grid[i][i]:
                path = dijkstra_shortest_path(weight_grid, self.state, i)
                if path[-1][1] != -1:
                    l_cost.append((path[1][0], path[-1][1]))  # set the cost for the entire path and the next step
        return l_cost

    def find_sheleter(self, sim=HurricaneSimulator()):
        shelter_nodes = sim.get_shelter()
        return self.search_grid(shelter_nodes, sim)

    def find_people(self, sim=HurricaneSimulator()):
        people_nodes = sim.get_people()
        return self.search_grid(people_nodes, sim)

    def choose_next_option(self, sim=HurricaneSimulator()):
        self.set_state(sim.get_state())

        cost_to_people = self.find_people(sim)  # Find costs for all vertices with people
        cost_to_shelter = self.find_sheleter(sim) if sim.people_in_vehicle else []  # Find costs for all shelter vertices

        """ Find best op """
        best_op = (-1, inf)
        for cost in cost_to_people:
            if cost[1] < best_op[1]:
                best_op = cost

        for cost in cost_to_shelter:
            if cost[1] < best_op[1]:
                best_op = cost

        return best_op[0]


