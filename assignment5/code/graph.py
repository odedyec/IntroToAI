from vertex import Vertex
from edge import Edge
from prob_lib import P


class Graph:
    """
    This is the basis object that holds all the information of vertices and edges
    """
    def __init__(self, num_of_vertices):
        self.deadline = 0.
        self._loc = 0
        self._num_of_vertices = num_of_vertices
        self._vertices = []
        self._edges = []
        for i in range(num_of_vertices):
            self._vertices.append(Vertex(i))

    def set_loc(self, loc):
        self._loc = loc

    def set_vertex_ev(self, vertex, num_of_ev):
        self._vertices[vertex].set_evacuess(num_of_ev)

    def set_vertex_is_shelter(self, vertex):
        self._vertices[vertex].set_shelter()

    def set_edge(self, vertex1, vertex2, weight, id, blockage):
        e = Edge(id, self._vertices[vertex1], self._vertices[vertex2], weight, blockage)
        self._vertices[vertex1].add_edge(e)
        self._vertices[vertex2].add_edge(e)
        self._edges.append(e)

    def __str__(self):
        s = ''
        for e in self._edges:
            s += "Edge {}: V{}({}) <-> V{}({}) --- W={}, P_blockage={}\n".format(e.id,
                                                                                 e.v1.id, e.v1.evacuees,
                                                                                 e.v2.id, e.v2.evacuees,
                                                                                 e.weight, P(e.blockage))
        return s