from graph import Graph
from prob_lib import *


class Simulator(Graph):
    def __init__(self, num_of_v):
        Graph.__init__(self, num_of_v)
        self._in_v = 0
        self._state = None
        self.saved = 0

    def build_state_when_finished_loading_graph(self):
        """  (Loc, Time, Saved, V1_with_people, V2_with_people, ..., Blockage_p_1, Blockage_p_2, ... )   """
        evs = [v for v in self.get_vertices() if v.evacuees]
        bs = [e for e in self.get_edges() if 0<P(e.blockage)<1]
        self._state = [self._loc, evs, bs, self.deadline, self.saved]

    def __str__(self):
        s = "({}, ".format(self._state[0])
        for ev in self._state[1]:
            s += str(ev) + ", "
        for e in self._state[2]:
            s += str(e) + ", "
        s += "{}, {})".format(self._state[3], self._state[4])
        return s

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


