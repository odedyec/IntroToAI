from evacuees import Evacuees
from blockage import Blockage
from prob_lib import ProbVar
import itertools


class Vertex:
    """
    A vertex object with all the associated information such as flooding probability and probability for evacuees
    """
    def __init__(self, id, num_of_vertices, flood=0.):
        self.id = id
        self.flood_p = ProbVar(flood)
        self._edges = []
        self._num_of_vertices = num_of_vertices
        self.evacuees = Evacuees([], [])
        self._evacuees_reported = None

    def set_flood_prob(self, f):
        self.flood_p = ProbVar(f)

    def add_edge(self, edge):
        """
        An add edge method that connects two vertices together.
        ASSUMPTION!!!! all edges are unblocked at first!!!
        :param edge: An edge object that connects this vertex to a different vertex.
        """
        self._edges.append(edge)
        self.evacuees = Evacuees(
            [edge.weight for edge in self._edges],
            [None] * len(self._edges)
        )

    def get_edge_list(self):
        edges = []
        for edge in self._edges:
            if edge.v1 is self:
                edges.append(edge.v2.id)
            else:
                edges.append(edge.v1.id)
        return edges

    def print_prob_for_flood(self):
        print ("P(Flood)={}\n".format(self.flood_p))

    def print_prob_for_evacuees(self):
        self.evacuees.print_conditional_prob(self._edges)

    def reset(self):
        self.evacuees.update_blockages([None] * len(self._edges))

    def evacuees_reported(self):
        self._evacuees_reported = True

    def flood_reported(self):
        for edge in self._edges:
            if self.id == edge.v1.id:
                current_flooding_situation = edge.blockage.floodings
                current_flooding_situation[0] = True
                edge.blockage.update_floodings(current_flooding_situation)
            else:
                current_flooding_situation = edge.blockage.floodings
                current_flooding_situation[1] = True
                edge.blockage.update_floodings(current_flooding_situation)

    def __str__(self):
        s = 'Vertex{}\n'.format(self.id)
        s += "---------\n"
        s += ("P(Flood)={}\n".format(self.flood_p))
        f_n = (-self.flood_p)
        s += ("P(!Flood)={}\n".format(f_n))
        for twice in [True, False]:
            for perm in list(itertools.product([False, True], repeat=len(self._edges))):
                if twice:
                    s += "P(Evacuees|"
                else:
                    s += "P(!Evacuees|"
                for p, e in zip(perm, self._edges):
                    s += "Blockage{} ".format(e.id) if p else "!Blockage{} ".format(e.id)
                if twice:
                    s += ')={}\n'.format(Evacuees([b.weight for b in self._edges], perm))
                else:
                    s += ')={}\n'.format((-Evacuees([b.weight for b in self._edges], perm)))
        return s


if __name__ == '__main__':
    v = Vertex(3, 2, 0.2)
    print str(v)
