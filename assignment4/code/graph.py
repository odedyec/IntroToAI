from vertex import Vertex


class Graph:
    def __init__(self, num_of_vertices):
        self._num_of_vertices = num_of_vertices
        self._graph = []
        for i in range(num_of_vertices):
            self._graph.append(Vertex(i, num_of_vertices))

    def __str__(self):
        return ('\n'.join([''.join(["  {}".format(str(ver)) if i == v else '{:14}'.format(ver.edge_weight(v)) for v in range(self._num_of_vertices)])
                         for i, ver in enumerate(self._graph)]))

    def set_vertex_people(self, vertex, people_prob):
        self._graph[vertex].set_people_prob(people_prob)

    def set_vertex_flood(self, vertex, flood_prob):
        self._graph[vertex].set_flood_prob(flood_prob)

    def set_edge(self, vertex1, vertex2, weight):
        self._graph[vertex1].set_edge_weight(vertex2, weight)
        self._graph[vertex2].set_edge_weight(vertex1, weight)


if __name__ == '__main__':
    g = Graph(4)
    print(str(g))