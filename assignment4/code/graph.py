from vertex import Vertex
from blockage import Blockage
from edge import Edge
from prob_lib import P
import itertools


class Graph:
    """
    This is the basis object that holds all the information of vertices and edges
    """
    def __init__(self, num_of_vertices):
        self._num_of_vertices = num_of_vertices
        self._vertices = []
        self._edges = []
        for i in range(num_of_vertices):
            self._vertices.append(Vertex(i, num_of_vertices))

    def set_vertex_flood(self, vertex, flood_prob):
        self._vertices[vertex].set_flood_prob(flood_prob)

    def set_edge(self, vertex1, vertex2, weight, id):
        e = Edge(id, self._vertices[vertex1], self._vertices[vertex2], weight)
        self._vertices[vertex1].add_edge(e)
        self._vertices[vertex2].add_edge(e)
        self._edges.append(e)

    def print_vertices(self, list_of_vertices=None):
        for v in self._vertices:
            if list_of_vertices is None or v.id in list_of_vertices:
                print(str(v))

    def print_edges(self, list_of_edges=None):
        for edge in self._edges:
            if list_of_edges is None or edge.id in list_of_edges:
                print (str(edge))

    def path_free_of_blockages(self, list_of_edges=None):
        prob = 1
        path_vertices = []
        for edge in self._edges:
            if list_of_edges is not None and edge.id in list_of_edges:
                prob *= P(-edge.blockage)
                print("prob= ", prob)
                for v in [edge.v1, edge.v2]:
                    if not (v in path_vertices):
                        prob *= P(v.flood_p)
                        path_vertices.append(v)

        print("The probability that the given path is free from blockages is ", prob)



if __name__ == '__main__':
    g = Graph(4)
    print(str(g))
    g.print_vertices()