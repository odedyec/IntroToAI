from vertex import Vertex
from blockage import Blockage
from edge import Edge
from prob_lib import P
import itertools
import json


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

        prob = 0
        vertices_indices = []

        for v in self._vertices:
            vertices_indices.append(v.id)

        for perm in list(itertools.product([False, True], repeat=len(vertices_indices))):
            temp_prob = 1

            for v in self._vertices:
                temp_prob *= P(v.flood_p) if perm[vertices_indices.index(v.id)] else P(-v.flood_p)

            for edge in self._edges:
                if list_of_edges is not None and edge.id in list_of_edges:
                    flooding_temp = [perm[vertices_indices.index(edge.v1.id)], perm[vertices_indices.index(edge.v2.id)]]
                    blockage_temp = Blockage(edge.id, edge.weight, flooding_temp, [edge.v1, edge.v2])

                    temp_prob *= (1 - blockage_temp.noisy_or(flooding_temp))
            prob += temp_prob

        print("The probability that the given path is free from blockages is ", prob)



if __name__ == '__main__':
    g = Graph(4)
    print(str(g))
    g.print_vertices()