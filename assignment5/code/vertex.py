
class Vertex:
    """
    A vertex object with all the associated information such as flooding probability and probability for evacuees
    """
    def __init__(self, id):
        self.id = id
        self._edges = []
        self.evacuees = 0
        self.is_shelter = False

    def set_shelter(self):
        self.is_shelter = True

    def set_evacuess(self, ev):
        self.evacuees = ev

    def add_edge(self, edge):
        """
        An add edge method that connects two vertices together.
        ASSUMPTION!!!! all edges are unblocked at first!!!
        :param edge: An edge object that connects this vertex to a different vertex.
        """
        self._edges.append(edge)

    def get_edge_list(self):
        edges = []
        for edge in self._edges:
            if edge.v1 is self:
                edges.append(edge.v2.id)
            else:
                edges.append(edge.v1.id)
        return edges

    def __str__(self):
        return str(self.id)

