class Vertex:
    def __init__(self, id, num_of_vertices, flood=0., people=0.):
        self.id = id
        self.flood_p = flood
        self.people_p = people
        self._edges = [-1] * num_of_vertices

    def set_flood_prob(self, f):
        self.flood_p = f

    def set_people_prob(self, p):
        self.people_p = p

    def set_edge_weight(self, vertex, weight):
        self._edges[vertex] = weight

    def set_all_data(self, flood, people, edges=None):
        self.set_flood_prob(flood)
        self.set_people_prob(people)
        if edges is None:
            return
        if len(edges) != len(self._edges):
            raise Exception("length of edges is different than number of vertices")
        self._edges = edges

    def edge_weight(self, vertex):
        return self._edges[vertex]

    def __neg__(self):
        v = Vertex(self.id, len(self._edges), 1 - self.flood_p, 1 - self.people_p)
        v._edges = self._edges
        return v

    def __str__(self):
        return ("({}%, {}%)").format(self.flood_p, self.people_p)


if __name__ == '__main__':
    v = Vertex(3, 2, 0.2, 0.4)
    print str(v)
    n_v = -v
    print str(n_v)
