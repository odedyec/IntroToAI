from simulator import HurricaneSimulator
from a_star_agent import A_Star
from smart_greedy_agent import Node
import copy


# PEOPLE_UNSAVED_VALUE = 100


class Real_Time_A_Star(A_Star):

    def __init__(self, state, expands=5):
        super(Real_Time_A_Star, self).__init__(state)
        self.max_expands = expands

    def choose_next_option(self, sim=HurricaneSimulator()):
        self.set_state(sim.get_state())
        #
        # precalculated_answer = self.check_if_path_ready(sim)
        # if precalculated_answer != -1:
        #     return precalculated_answer

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
            best_state = best_child.state
            best_sim = best_child.sim
            current_tree_node = best_child
            self.expanded_nodes += 1
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




