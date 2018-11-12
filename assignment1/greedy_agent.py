from agent import BaseAgent
from simulator import HurricaneSimulator
from numpy import inf
from shortest_path import dijkstra_shortest_path


class Greedy(BaseAgent):

    def search_grid(self, grid, sim=HurricaneSimulator()):
        """
        This function performs the actual search in a grid, and calculates the cost to each vertex of interest
        :param grid: people or shelter grid
        :param sim: the environment
        :return: list of tuples: (next vertex, cost to final destination, final destination)
        """
        l_cost = []
        weight_grid = sim.get_weights()
        for i in range(sim.num_of_vertices):
            if grid[i][i]:
                path, depth_searched = dijkstra_shortest_path(weight_grid, sim.get_state(), i)
                # self.steps_explored += depth_searched
                if len(path) == 1:
                    """ Already at a shelter town """
                    l_cost.append((path[0][0], 0, path[0][0]))
                elif path[-1][1] != -1:
                    l_cost.append((path[1][0], path[-1][1], path[-1][0]))  # set the cost for the entire path and the next step
        return l_cost

    def find_shelter(self, sim=HurricaneSimulator()):
        """
        This function finds the cost to all shelter nodes
        :param sim:  the environment
        :return: list of tuples: (next vertex, cost to final destination)
        """
        shelter_nodes = sim.get_shelter()
        return self.search_grid(shelter_nodes, sim)

    def find_people(self, sim=HurricaneSimulator()):
        """
        This function finds the cost to all nodes with people
        :param sim:  the environment
        :return: list of tuples: (next vertex, cost to final destination)
        """
        people_nodes = sim.get_people()
        return self.search_grid(people_nodes, sim)

    def choose_next_option(self, sim=HurricaneSimulator()):
        """
        next option greedy choice. Searches through all possible options to reach shelter (if people in vehicle) and
        vertices with people
        :param sim:
        :return: Best next option. This agent is optimal
        """
        self.set_state(sim.get_state())

        cost_to_people = self.find_people(sim)  # Find costs for all vertices with people
        cost_to_shelter = self.find_shelter(sim) if sim.people_in_vehicle else []  # Find costs for all shelter vertices

        """ Find best op """
        best_op = (-1, inf)
        for cost in cost_to_people:
            if cost[1] < best_op[1]:
                best_op = cost

        for cost in cost_to_shelter:
            if cost[1] < best_op[1]:
                best_op = cost

        return best_op[0]


