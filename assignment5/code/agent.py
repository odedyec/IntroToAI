from graph import Graph
from prob_lib import *


class Agent(Graph):
    def __init__(self, num_of_v):
        Graph.__init__(self, num_of_v)
        self._in_v = 0
        self._state = None
        self.saved = 0

    def build_state_when_finished(self):
        """  (Loc, Time, Saved, V1_with_people, V2_with_people, ..., Blockage_p_1, Blockage_p_2, ... )   """
        evs = [v for v in self._vertices if v.evacuees]
        bs = [v for e in self._edges if 0<P(e.blockage)<1]
        self._state = (self._loc, self.deadline, self.saved, evs, bs)

