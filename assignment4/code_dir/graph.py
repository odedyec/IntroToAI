from vertex import Vertex
from edge import Edge
from prob_lib import P
from copy import deepcopy


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



# if __name__ == '__main__':
#     g = Graph(4)
#     print(str(g))
#     g.print_vertices()
