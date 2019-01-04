from graph import Graph
from prob_lib import *
from copy import deepcopy
import sys

sys.setrecursionlimit(150000)


LARGE_NUMBER = 1000


class Simulator(Graph):
    STATE_LOC = 0
    STATE_PEOPLE_LIST = 4
    STATE_BLOCKAGE_LIST = 5
    STATE_TIME_LEFT = 1
    STATE_SAVED = 2
    STATE_IN_VEHICLE = 3

    def __init__(self, num_of_v):
        Graph.__init__(self, num_of_v)
        self._in_v = 0
        self._state = None
        self.saved = 0
        self.utility = None
        self.vertices_with_ev = None
        self.potential_blockages = None
        self.reward = 0
        self.rec_num = 0

    def state_builder(self, v_to_move, edge_to_cross, blockage_list, state):
        saved_now = state[self.STATE_IN_VEHICLE] if self.is_vertex_shelter(v_to_move) else 0
        ev_list, picked_up_now = self.get_evacuees_state(v_to_move, state[self.STATE_PEOPLE_LIST])
        new_state = (
            v_to_move,
            max(state[self.STATE_TIME_LEFT] - edge_to_cross.weight, 0),
            state[self.STATE_SAVED] + saved_now,
            0 if saved_now else state[self.STATE_IN_VEHICLE] + picked_up_now,
            ev_list,
            blockage_list
        )
        return new_state

    def get_evacuees_state(self, new_loc, old_state=None):
        if old_state is None:
            old_state = [True] * len(self.vertices_with_ev)
        ans = list(old_state)
        picked_up = 0
        for i, v in enumerate(self.vertices_with_ev):
            if v.id == new_loc and ans[i]:
                ans[i] = False
                picked_up = v.evacuees
        return tuple(ans), picked_up

    def get_blockages_permutations_and_probs(self, new_loc, old_state=None):
        if old_state is None:
            old_state = [None] * len(self.potential_blockages)
        perms = [list(old_state)]
        probs = [1.]
        for i, e in enumerate(self.potential_blockages):
            if (e.v1.id == new_loc or e.v2.id == new_loc) and old_state[i] is None:
                new_perms = []
                new_probs = []
                for p, perm in zip(probs, perms):
                    perm[i] = True
                    new_probs.append(p * P(e.blockage))
                    new_perms.append(deepcopy(perm))
                    perm[i] = False
                    new_probs.append(p * (1 - P(e.blockage)))
                    new_perms.append(deepcopy(perm))
                perms = new_perms
                probs = new_probs
        return [tuple(perm) for perm in perms], probs

    def get_blockages_state(self, new_loc, old_state=None):
        if old_state is None:
            old_state = [None] * len(self.potential_blockages)
        ans = list(old_state)
        for i, e in enumerate(self.potential_blockages):
            if (e.v1.id == new_loc or e.v2.id == new_loc) and old_state[i] is None:
                ans[i] = e.is_blocked()
        return tuple(ans)

    def is_state_terminal(self, state=None):
        if state is None:
            state = self._state
        if state[self.STATE_TIME_LEFT] <= 0:
            return True
        return False

    def get_terminal_reward(self, state):
        return state[self.STATE_SAVED] * LARGE_NUMBER

    def update_utility(self, new_table):
        diff = 0.
        for key in new_table:
            diff += abs(new_table[key] - self.utility[key])
        self.utility = new_table
        return diff

    def get_all_actions(self, state=None):
        if state is None:
            state = self._state
        edges = self.get_all_actions_for_vertex(state[self.STATE_LOC])
        action_list = []
        for edge in edges:
            add_edge = True
            for i, e in enumerate(self.potential_blockages):
                if e is edge:
                    if state[self.STATE_BLOCKAGE_LIST][i] is True:
                        add_edge = False
            if add_edge:
                action_list.append(edge.id)
        return action_list

    def recursive_build_utility(self, states):
        while len(states):
            state = states.pop(-1)
            if self.is_state_terminal(state):
                self.utility[state] = self.get_terminal_reward(state)
                continue
            self.utility[state] = 0
            for action in self.get_all_actions(state):
                possible_states, _ = self.all_possible_states_and_probs_from_action(state, action)
                for new_state in possible_states:
                    states.append(new_state)

    def build_state_when_finished_loading_graph(self):
        """  (Loc, Time, Saved, V1_with_people, V2_with_people, ..., Blockage_p_1, Blockage_p_2, ... )   """
        self.vertices_with_ev = [v for v in self.get_vertices() if v.evacuees]
        self.potential_blockages = [e for e in self.get_edges() if 0<P(e.blockage)<1]
        ev_list, _ = self.get_evacuees_state(self.vertices_with_ev)
        self._state = (self._loc,
                       self.deadline,
                       self.saved,
                       self._in_v,
                       ev_list,
                       self.get_blockages_state(self.potential_blockages)
                       )
        self.utility = {}
        self.recursive_build_utility([self._state])

    def __str__(self):
        s = "(@{}, {}IV, {}Sav, {}[T], {}[U])".format(self._state[self.STATE_LOC],
                                                      self._state[self.STATE_IN_VEHICLE],
                                                      self._state[self.STATE_SAVED],
                                                      self._state[self.STATE_TIME_LEFT],
                                                      self.utility[self._state])
        return s

    def all_possible_states_and_probs_from_action(self, state, action):
        states = []
        edge_to_cross = self.get_edge_from_id(action)
        v_to_move = self.vertex_to_move_from_loc(state[self.STATE_LOC], edge_to_cross)
        blockages, probs = self.get_blockages_permutations_and_probs(v_to_move, state[self.STATE_BLOCKAGE_LIST])
        for blockage in blockages:
            new_state = self.state_builder(v_to_move, edge_to_cross, blockage, state)
            states.append(new_state)
        return states, probs

    def state_from_action(self, state, action):
        edge_to_cross = self.get_edge_from_id(action)
        v_to_move = self.vertex_to_move_from_loc(state[self.STATE_LOC], edge_to_cross)
        new_state = self.state_builder(v_to_move, edge_to_cross,
                                       self.get_blockages_state(v_to_move, state[self.STATE_BLOCKAGE_LIST]),
                                       state)
        return new_state

    def act_based_utility(self):
        best_utility = -10000
        best_action = None
        for action in self.get_all_actions(self._state):
            if self.get_edge_from_id(action).is_blocked():
                continue
            u = self.get_utility_for_action(self._state, action)
            if u > best_utility:
                best_action = action
                best_utility = u
        # self.apply_action(best_action)
        self._state = self.state_from_action(self._state, best_action)

    def get_utility_for_action(self, state, action):
        states, probs = self.all_possible_states_and_probs_from_action(state, action)

        utility = 0.0
        for new_state, prob in zip(states, probs):
            if not self.check_feasible_state(new_state):
                continue
            utility += self.utility[new_state] * prob
        return utility

    def check_feasible_state(self, state):
        if state[self.STATE_IN_VEHICLE] + state[self.STATE_SAVED] > self.sum_of_people:
            return False
        return True

