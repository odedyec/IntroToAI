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
            s += "Edge {}: V{}({}) <-> V{}({}) --- W={}, P_blockage={}, Blocked={}\n".format(e.id,
                                                                                 e.v1.id, e.v1.evacuees,
                                                                                 e.v2.id, e.v2.evacuees,
                                                                                 e.weight, P(e.blockage), e.is_blocked())
        print(s)

    def get_edges(self):
        return self._edges

    def get_vertices(self):
        return self._vertices

    def __str__(self):
        return 'Call print graph as string for now'

    def get_all_actions_for_vertex(self, vertex):
        for v in self._vertices:
            if v.id == vertex:
                return [e for e in v.get_edges()]

    def is_edge_blocked(self, edge_id):
        for edge in self._edges:
            if edge.id == edge_id:
                return edge.is_blocked()

    def get_action_success_prob(self, action):
        return P(self.get_edge_from_id(action).blockage)

    def get_edge_from_id(self, id):
        for edge in self._edges:
            if edge.id == id:
                return edge
        raise Exception("No Edge with ID {}".format(id))

    def get_vertex_from_id(self, id):
        for vertex in self._vertices:
            if vertex.id == id:
                return vertex
        raise Exception("No vertex with ID {}".format(id))

    def vertex_to_move_from_loc(self, loc, edge_to_cross):
        if edge_to_cross.v2.id == loc:
            v_to_move = edge_to_cross.v1.id
        elif edge_to_cross.v1.id == loc:
            v_to_move = edge_to_cross.v2.id
        else:
            raise Exception("Can't cross edge {}. I am at {}".format(edge_to_cross.id, loc))
        return v_to_move

    def find_edge_that_connects(self, v1, v2):
        for edge in self._edges:
            if edge.v1.id == v1 and edge.v2.id == v2:
                return edge
        raise Exception("No edge connects V{} and V{}".format(v1, v2))

    def get_num_of_people_at_vertex(self, vertex):
        for v in self._vertices:
            if v.id == vertex:
                return v.evacuees