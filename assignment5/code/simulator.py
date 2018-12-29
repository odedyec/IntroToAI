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

    def get_blockages_state(self, new_loc, old_state=None):
        if old_state is None:
            old_state = [None] * len(self.vertices_with_ev)
        ans = []
        for i, e in enumerate(self.potential_blockages):
            if e.v1.id == new_loc or e.v2.id == new_loc or old_state[i] is not None:
                ans.append(False)  #TODO change based on knowledge
            else:
                ans.append(None)
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
        diff = 8  #sum(map(lambda x: abs(x[1] - x[0]), zip(new_table, self.utility)))
        self.utility = new_table
        return diff

    def get_all_actions(self, state):
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
            for time in range(self.deadline):
                for saved in range(1+sum([v.evacuees for v in self.vertices_with_ev])):
                    for in_v in range(1+sum([v.evacuees for v in self.vertices_with_ev])):
                        for ev_perm in itertools.product([True, False], repeat=len(self.vertices_with_ev)):
                            for bs_perm in itertools.product([True, False, None], repeat=len(self.potential_blockages)):
                                state = (loc, time, saved, in_v, ev_perm, bs_perm)
                                if self.check_feasible_state(state):
                                    self.utility[state] = 0.

    def __str__(self):
        s = "(@{}, {}IV, {}Sav,{}[T])".format(self._state[self.STATE_LOC], self._state[self.STATE_IN_VEHICLE], self._state[self.STATE_SAVED], self._state[self.STATE_TIME_LEFT])
        return s

    def state_from_action(self, state, action):
        for edge in self.get_edges():
            if edge.id == action:
                edge_to_cross = edge
                break
        if edge_to_cross.v2.id == state[self.STATE_LOC]:
            v_to_move = edge_to_cross.v1.id
        elif edge_to_cross.v1.id == state[self.STATE_LOC]:
            v_to_move = edge_to_cross.v2.id
        else:
            raise Exception("Can't cross edge {}. I am at {}".format(edge_to_cross.id, state[self.STATE_LOC]))

        saved_now = state[self.STATE_IN_VEHICLE] if self.is_vertex_shelter(v_to_move) else 0
        picked_up_now = 0
        for i, v in enumerate(self.vertices_with_ev):
            if v.id == v_to_move:
                picked_up_now = v.evacuees if state[self.STATE_PEOPLE_LIST][i] else 0
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
            u = self.get_utility_for_action(self._state, action)
            if u > best_utility:
                best_action = action
                best_utility = u
        self._state = self.state_from_action(self._state, best_action)

    def apply_action(self, edge_to_cross):
        for edge in self.get_edges():
            if edge.id == edge_to_cross:
                edge_to_cross = edge
                break
        if edge_to_cross.v2.id == self._state[0]:
            v_to_move = edge_to_cross.v1.id
        elif edge_to_cross.v1.id == self._state[0]:
            v_to_move = edge_to_cross.v2.id
        else:
            raise Exception("Can't cross edge {}. I am at {}".format(edge_to_cross.id, self._state[0]))
        self.set_loc(v_to_move)
        self._state[0] = v_to_move
        self._state[3] -= edge_to_cross.weight
        if self.get_vertices()[v_to_move].evacuees:
            self._in_v += self.get_vertices()[v_to_move].evacuees
            self.get_vertices()[v_to_move].evacuees = 0
        for e in self.get_vertices()[v_to_move].get_edges():
            if e.blockage_unclear():
                e.set_blockage_from_knowledge()

    def get_utility_for_action(self, state, action):
        new_state = self.state_from_action(state, action)
        if self.check_feasible_state(new_state):
            return self.utility[new_state]
        return 0

    def check_feasible_state(self, state):
        if state[self.STATE_IN_VEHICLE] + state[self.STATE_SAVED] > self.sum_of_people:
            return False
        return True


