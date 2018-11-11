from greedy_agent import Greedy
from agent import BaseAgent
from simulator import HurricaneSimulator
from numpy import inf
from shortest_path import dijkstra_shortest_path
from smart_greedy_agent import SmartGreedy
from smart_greedy_agent import Node
from agent import BaseAgent
import copy


# PEOPLE_UNSAVED_VALUE = 100


class A_Star(SmartGreedy):

    def __init__(self, state):
        super(A_Star, self).__init__(state)
        self.max_expands = inf

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
            if best_child.g_score + best_child.h_score > child.g_score + child.h_score:
                best_child = child
        return best_child

    def choose_next_option(self, sim=HurricaneSimulator()):

        self.set_state(sim.get_state())

        if self.check_if_path_ready(sim) != -1:
            return self.check_if_path_ready(sim)

        best_state = self.build_full_state(sim)
        best_sim = copy.deepcopy(sim)
        tree = Node(state=best_state, sim=sim)
        best_child = tree
        best_path = list()
        nodes_not_expanded = [tree]
        current_tree_node = tree
        expands_in_this_search = 0

        while not self.is_goal(best_state, best_sim) and self.max_expands > expands_in_this_search:
            """ Expand the current node """
            nodes_not_expanded.remove(current_tree_node)

            """ Explore all options"""
            actions = self.get_all_possible_actions(best_sim)
            for action in actions:
                sim_emulation = copy.deepcopy(best_sim)  # Not actually required for greedy search, but for A*
                sim_emulation.apply_action(action[0])
                nodes_not_expanded.append(Node(state=self.build_full_state(sim_emulation), sim=sim_emulation,
                                               g=current_tree_node.g_score + action[1],
                                               h=self.calculate_heuristic_for_action(action[1], sim_emulation),
                                               p=current_tree_node))

            """ Find best child """
            best_child = self.find_best_branch_to_explore(nodes_not_expanded)
            ## TODO check if there are two children with the same values. Both should be explred.
            best_state = best_child.state
            best_sim = best_child.sim
            current_tree_node = best_child
            self.steps_explored += 1
            expands_in_this_search += 1

        """ No possible way to expand """
        if best_child == tree:
            return -1

        current_tree_node = best_child
        while current_tree_node != tree:
            best_path.insert(0, current_tree_node.state)
            current_tree_node = current_tree_node.parent
        self.path = best_path
        return self.path.pop(0)['state']




