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
        self._evidence_list = []

    def enumeration_ask(self, query_var, evidence):
        q = []
        for (e, e_v) in evidence:
            if e.get_name() == query_var.get_name():
                q.append(1 if e_v else 0)
                q.append(1 - q[0])
                return q

        vars_list = []
        for vertex in self._vertices:
            vars_list.append(vertex.flood_p)
        for edge in self._edges:
            vars_list.append(edge.blockage)
        for vertex in self._vertices:
            vars_list.append(vertex.evacuees)

        hidden_vars_and_query = []
        for var in vars_list:
            if var.get_name() not in [e.get_name() for (e, e_v) in evidence]:
                hidden_vars_and_query.append(var)

        for query_val in [True, False]:
            evidence_x = list(evidence)
            evidence_x.append((query_var, query_val))
            x_prob = self.enumerate_all(hidden_vars_and_query, evidence_x)
            q.append(x_prob)
        return [i / sum(q) for i in q]

    def enumerate_all(self, vars, evidence):
        if len(vars) == 0:
            return 1
        vars_copy = list(vars)
        Y = vars_copy.pop(0)
        for (Y_var, y_val) in evidence:
            if Y_var.get_name() == Y.get_name():
                prob = Y.calc_prob_from_evidence(evidence)
                prob = prob if y_val else 1-prob
                return prob * self.enumerate_all(vars_copy, evidence)

        sigma = 0
        for y_v in [True, False]:
            prob = Y.calc_prob_from_evidence(evidence)
            prob = prob if y_v else 1-prob
            evidence_y = list(evidence)
            evidence_y.append((Y, y_v))
            prob_y_v = prob * self.enumerate_all(vars_copy, evidence_y)
            sigma += prob_y_v
        return sigma

    def set_vertex_flood(self, vertex, flood_prob):
        self._vertices[vertex].set_flood_prob(flood_prob)

    def set_edge(self, vertex1, vertex2, weight, id):
        e = Edge(id, self._vertices[vertex1], self._vertices[vertex2], weight)
        self._vertices[vertex1].add_edge(e)
        self._vertices[vertex2].add_edge(e)
        self._edges.append(e)

    def print_vertices(self, list_of_vertices=None):
        copy = deepcopy(self)
        for v in copy._vertices:
            if list_of_vertices is None or v.id in list_of_vertices:
                print(str(v))
                q = copy.enumeration_ask(v.evacuees, copy._evidence_list)
                print("P(Evacuees {} | {}) = {}\n".format(v.id, [(i.get_name() if j else "! " + i.get_name()) for
                                                                 (i, j) in self._evidence_list], q[0]))

    def print_edges(self, list_of_edges=None):
        copy = deepcopy(self)
        for edge in copy._edges:
            if list_of_edges is None or edge.id in list_of_edges:
                print(str(edge))
                q = copy.enumeration_ask(edge.blockage, copy._evidence_list)
                print("P(Blockage {} | {}) = {}\n".format(edge.id, [(i.get_name() if j else "! " + i.get_name()) for
                                                                 (i, j) in self._evidence_list], q[0]))

    def path_free_of_blockages(self, list_of_edges=None):
        prob = 1
        copy = deepcopy(self)
        for edge in copy._edges:
            if list_of_edges is None or edge.id in list_of_edges:
                q = copy.enumeration_ask(edge.blockage, copy._evidence_list)
                prob *= q[1]  # probability that edge.blockage is false
                edge.blockage_reported(False)
                copy._evidence_list.append((edge.blockage, False))
        print("\n------------")
        print("The probability that the given path is free from blockages is {}\n------------".format(prob))


# if __name__ == '__main__':
#     g = Graph(4)
#     print(str(g))
#     g.print_vertices()
