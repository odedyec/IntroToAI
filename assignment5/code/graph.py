from vertex import Vertex
from edge import Edge
from prob_lib import P


class Graph:
    """
    This is the basis object that holds all the information of vertices and edges
    """
    def __init__(self, num_of_vertices):
        self.sum_of_people = 0
        self.deadline = 0.
        self._loc = 0
        self._num_of_vertices = num_of_vertices
        self._vertices = []
        self._edges = []
        for i in range(num_of_vertices):
            self._vertices.append(Vertex(i))

    def is_vertex_shelter(self, vertex):
        for v in self._vertices:
            if v.id == vertex:
                return v.is_shelter

    def pick_up(self, vertex):
        for v in self._vertices:
            if v.id == vertex:
                return v.evacuees

    def set_loc(self, loc):
        self._loc = loc

    def set_vertex_ev(self, vertex, num_of_ev):
        self.sum_of_people += num_of_ev
        self._vertices[vertex].set_evacuess(num_of_ev)

    def set_vertex_is_shelter(self, vertex):
        self._vertices[vertex].set_shelter()

    def set_edge(self, vertex1, vertex2, weight, id, blockage):
        e = Edge(id, self._vertices[vertex1], self._vertices[vertex2], weight, blockage)
        self._vertices[vertex1].add_edge(e)
        self._vertices[vertex2].add_edge(e)
        self._edges.append(e)

    def print_graph_as_string(self):
        s = ''
        for e in self._edges:
            s += "Edge {}: V{}({}) <-> V{}({}) --- W={}, P_blockage={}\n".format(e.id,
                                                                                 e.v1.id, e.v1.evacuees,
                                                                                 e.v2.id, e.v2.evacuees,
                                                                                 e.weight, P(e.blockage))
        print s

    def get_edges(self):
        return self._edges

    def get_vertices(self):
        return self._vertices

    def __str__(self):
        return 'Call print graph as string for now'

    def get_all_actions_for_vertex(self, vertex):
        for v in self._vertices:
            if v.id == vertex:
                return [e.id for e in v.get_edges()]