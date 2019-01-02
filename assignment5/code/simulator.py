from graph import Graph
from prob_lib import *


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

    def get_evacuees_state(self, new_loc, old_state=None):
        if old_state is None:
            old_state = [True] * len(self.vertices_with_ev)
        ans = []
        for i, v in enumerate(self.vertices_with_ev):
            if v.id == new_loc or not old_state[i]:
                ans.append(False)
            else:
                ans.append(True)
        return tuple(ans)

    def get_blockages_state(self, new_loc, old_state=None, value_of_blockage=None):
        if old_state is None:
            old_state = [None] * len(self.potential_blockages)
        ans = list(old_state)
        for i, e in enumerate(self.potential_blockages):
            if e.v1.id == new_loc or e.v2.id == new_loc or old_state[i] is not None:
                ans[i] = e.is_blocked() if value_of_blockage is None else value_of_blockage
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
        if state == None:
            loc = self._state[self.STATE_LOC]
        else:
            loc = state[self.STATE_LOC]
        return self.get_all_actions_for_vertex(loc)

    def build_state_when_finished_loading_graph(self):
        """  (Loc, Time, Saved, V1_with_people, V2_with_people, ..., Blockage_p_1, Blockage_p_2, ... )   """
        self.vertices_with_ev = [v for v in self.get_vertices() if v.evacuees]
        self.potential_blockages = [e for e in self.get_edges() if 0<P(e.blockage)<1]
        self._state = (self._loc,
                       self.deadline,
                       self.saved,
                       self._in_v,
                       self.get_evacuees_state(self.vertices_with_ev),
                       self.get_blockages_state(self.potential_blockages)
                       )
        self.utility = {}
        for loc in range(self._num_of_vertices):
            for time in range(self.deadline+1):
                for saved in range(1+sum([v.evacuees for v in self.vertices_with_ev])):
                    for in_v in range(1+sum([v.evacuees for v in self.vertices_with_ev])):
                        for ev_perm in itertools.product([True, False], repeat=len(self.vertices_with_ev)):
                            for bs_perm in itertools.product([True, False, None], repeat=len(self.potential_blockages)):
                                state = (loc, time, saved, in_v, ev_perm, bs_perm)
                                if self.check_feasible_state(state):
                                    self.utility[state] = 0.

    def __str__(self):
        s = "(@{}, {}IV, {}Sav, {}[T], {}[U])".format(self._state[self.STATE_LOC],
                                                      self._state[self.STATE_IN_VEHICLE],
                                                      self._state[self.STATE_SAVED],
                                                      self._state[self.STATE_TIME_LEFT],
                                                      self.utility[self._state])
        return s

    def state_from_action(self, state, action, actually_moved=False):
        edge_to_cross = self.get_edge_from_id(action)
        v_to_move = self.vertex_to_move_from_loc(state[self.STATE_LOC], edge_to_cross)

        saved_now = state[self.STATE_IN_VEHICLE] if self.is_vertex_shelter(v_to_move) else 0
        picked_up_now = 0
        for i, v in enumerate(self.vertices_with_ev):
            if v.id == v_to_move:
                picked_up_now = v.evacuees if state[self.STATE_PEOPLE_LIST][i] else 0
        if not actually_moved:
            new_state1 = (
                v_to_move,
                max(state[self.STATE_TIME_LEFT] - edge_to_cross.weight, 0),
                state[self.STATE_SAVED] + saved_now,
                0 if saved_now else state[self.STATE_IN_VEHICLE] + picked_up_now,
                self.get_evacuees_state(v_to_move, state[self.STATE_PEOPLE_LIST]),
                self.get_blockages_state(v_to_move, state[self.STATE_BLOCKAGE_LIST], value_of_blockage=True)
            )
            new_state2 = (
                v_to_move,
                max(state[self.STATE_TIME_LEFT] - edge_to_cross.weight, 0),
                state[self.STATE_SAVED] + saved_now,
                0 if saved_now else state[self.STATE_IN_VEHICLE] + picked_up_now,
                self.get_evacuees_state(v_to_move, state[self.STATE_PEOPLE_LIST]),
                self.get_blockages_state(v_to_move, state[self.STATE_BLOCKAGE_LIST], value_of_blockage=False)
            )
            return new_state1, new_state2
        else:
            new_state = (
                v_to_move,
                max(state[self.STATE_TIME_LEFT] - edge_to_cross.weight, 0),
                state[self.STATE_SAVED] + saved_now,
                0 if saved_now else state[self.STATE_IN_VEHICLE] + picked_up_now,
                self.get_evacuees_state(v_to_move, state[self.STATE_PEOPLE_LIST]),
                self.get_blockages_state(v_to_move, state[self.STATE_BLOCKAGE_LIST])
            )
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
        self._state = self.state_from_action(self._state, best_action, actually_moved=True)

    def get_utility_for_action(self, state, action):
        edge = self.get_edge_from_id(action)
        for i, edge_p in enumerate(self.potential_blockages):
            if edge is edge_p:
                if state[self.STATE_BLOCKAGE_LIST][i] is True:
                    return 0.
        new_state_true, new_state_false = self.state_from_action(state, action, actually_moved=False)
        if not self.check_feasible_state(new_state_false):
            return 0

        prob = 0.
        for i, edge_p in enumerate(self.potential_blockages):
            if new_state_true[self.STATE_BLOCKAGE_LIST][i] is True and state[self.STATE_BLOCKAGE_LIST][i] is None:
                prob = P(edge_p.blockage)

        u_false = self.utility[new_state_false]
        u_true = self.utility[new_state_true]
        return u_false * (1 - prob) + u_true * prob

    def check_feasible_state(self, state):
        if state[self.STATE_IN_VEHICLE] + state[self.STATE_SAVED] > self.sum_of_people:
            return False
        return True

_state = self.state_from_action(self._state, edge_to_cross.id)