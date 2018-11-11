from greedy_agent import Greedy
from agent import BaseAgent
from simulator import HurricaneSimulator
from numpy import inf
from shortest_path import dijkstra_shortest_path
import copy


PEOPLE_UNSAVED_VALUE = 100

class Node(object):
    def __init__(self, state=None, sim=None, g=0, h=0):
        self.children = list()
        self.state = state
        self.sim = sim
        self.h_score = h  # Heuristic value of node
        self.g_score = g  # Actual value (for A*)


class SmartGreedy(Greedy):
    def get_all_possible_actions(self, sim=HurricaneSimulator()):
        """
        Find all possible actions from a specific node
        :param sim: an environment
        :return: a list of tuples. Each tuple is:
        (the vertex to go to, the cost to that vertex (for A*), the heuristic of the vertex)
        """
        weights = sim.get_weights()
        actions = []
        for vertex, cost in enumerate(weights[sim.get_state()]):
            if cost != -1:
                action = (vertex, cost)
                actions.append(action)
        return actions

    def calculate_heuristic_for_action(self, cost, sim=HurricaneSimulator()):
        """
        This function calculates the heuristic for a single.
        :param vertex: the vertex to which you wish to calculate the heuristic
        :param sim: the environment
        :return: a heuristic value
        """
        number_of_people_in_towns = sim.get_number_of_people_in_towns()
        people_unable_to_save = number_of_people_in_towns + sim.people_in_vehicle
        cost_to_people = self.find_people(sim)  # Find costs for all vertices with people
        cost_to_shelter = self.find_sheleter(sim)  # Find costs for all shelter vertices

        if len(cost_to_shelter) == 0:
            """ No shelter, we are all doomed :("""
            return cost + people_unable_to_save * PEOPLE_UNSAVED_VALUE
        """ Find closest shelter """
        closest_shelter = inf
        for shelter in cost_to_shelter:
            if shelter[1] < closest_shelter:
                closest_shelter = shelter[1]
        if (1+ sim.K * sim.people_in_vehicle) * closest_shelter + sim.get_time() < sim.deadline:
            """ People in vehicle can be saved """
            people_unable_to_save -= sim.people_in_vehicle
        else:
            """ Unable to reach shelter """
            return cost + people_unable_to_save * PEOPLE_UNSAVED_VALUE
        """ Find people in towns """
        time_elapsed = sim.get_time()
        for people in cost_to_people:
            time_elapsed += people[1] + \
                            (1 +
                             sim.K * (sim.graph[people[2]][people[2]].num_of_people + sim.people_in_vehicle)) \
                            * (closest_shelter + people[1])
            if time_elapsed < sim.deadline:
                people_unable_to_save -= sim.graph[people[2]][people[2]].num_of_people
        return cost + people_unable_to_save * PEOPLE_UNSAVED_VALUE

    def is_goal(self, full_state, sim=HurricaneSimulator()):
        """
        Is a goal reached?
        A goal is run out the clock or best goal is saved all people
        :param full_state: as built by buil_full_state() method
        :param sim:
        :return: true if goal or false
        """
        if full_state['number_of_people_to_save'] == 0:
            """ Reached optimal goal"""
            return True
        if full_state['time_passed'] >= sim.deadline:
            """ Run out of time :( """
            return True
        return False

    def build_full_state(self, sim=HurricaneSimulator()):
        """
        Build a full state to work with
        :param sim: the env
        :return: a dict with (state, time, list_of_vertices_with_people, number_of_people_to_save, number_of_people_in_vehicle)
        """
        """ Create a list of people vertices """
        list_of_vertices_with_people = []
        people = sim.get_people()
        sum_of_people = 0
        for i in range(sim.num_of_vertices):
            sum_of_people += people[i][i]
            if people[i][i]:
                data = (i, people[i][i])
                list_of_vertices_with_people.append(data)
        """ Create the full state """
        full_state = {'state': sim.get_state(), 'time_passed': sim.get_time(), 'list_of_vertices_with_people': list_of_vertices_with_people,
                      'number_of_people_to_save': sum_of_people+sim.people_in_vehicle, 'number_of_people_in_vehicle': sim.people_in_vehicle}
        return full_state

    def find_best_branch_to_explore(self, list_of_nodes=[Node()]):
        """
        This function gets a tree of possible states to go to
        :param states_and_sims:
        :return:
        """
        best_child = None
        for child in list_of_nodes:
            if best_child is None:
                best_child = child
                continue
            if best_child.h_score > child.h_score:
                best_child = child
        return best_child

    def choose_next_option(self, sim=HurricaneSimulator()):
        self.set_state(sim.get_state())
        """ Check precalculated path"""
        if self.check_if_path_ready(sim) != -1:
            return self.check_if_path_ready(sim)

        best_state = self.build_full_state(sim)
        best_sim = copy.deepcopy(sim)
        tree = Node(state=best_state, sim=sim)
        current_tree_node = tree

        while not self.is_goal(best_state, best_sim):
            """ Explore all options"""
            actions = self.get_all_possible_actions(best_sim)
            for action in actions:
                sim_emulation = copy.deepcopy(best_sim)  # Not actually required for greedy search, but for A*
                sim_emulation.apply_action(action[0])
                current_tree_node.children.append(Node(state=self.build_full_state(sim_emulation),
                                          sim=sim_emulation,
                                          g=action[1],
                                          h=self.calculate_heuristic_for_action(action[1], sim_emulation)))
            break
        final_action = self.find_best_branch_to_explore(tree.children)
        go_to_state = final_action.state['state'] if final_action is not None else -1
        return go_to_state


