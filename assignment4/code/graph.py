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
        vars = []
        for vertex in self._vertices:
            vars.append(vertex.flood_p)
        for edge in self._edges:
            vars.append(edge.blockage)
        for vertex in self._vertices:
            vars.append(vertex.evacuees)

        for query_val in [True, False]:
            evidence_x = evidence.copy()
            evidence_x.append((query_var, query_val))
            x_prob = self.enumerate_all(vars, evidence_x)
            # evidence.append((query_var, query_val))
            # x_prob = self.enumerate_all(vars, evidence)
            q.append(x_prob)
        return [i / sum(q) for i in q]

    def enumerate_all(self, vars, evidence):
        if not vars:  # if vars is empty
            return 1
        # vars_copy = vars.copy()
        Y = vars.pop(0)
        for (Y_var, y_val) in evidence:
            if Y_var.get_name() == Y.get_name():
                # prob = P(Y) if y_val else P(-Y)
                prob = Y.calc_prob_from_evidence(evidence)
                prob = prob if y_val else 1-prob
                return prob * self.enumerate_all(vars, evidence)

        sigma = 0
        for y_v in [True, False]:
            # prob = P(Y) if y_v else P(-Y)
            prob = Y.calc_prob_from_evidence(evidence)
            prob = prob if y_v else 1-prob
            evidence_y = evidence.copy()
            evidence_y.append((Y, y_v))
            sigma += prob * self.enumerate_all(vars, evidence_y)
            # evidence.append((Y, y_v))
            # sigma += prob * self.enumerate_all(vars, evidence)
        return sigma

    def set_vertex_flood(self, vertex, flood_prob):
        self._vertices[vertex].set_flood_prob(flood_prob)

    def set_edge(self, vertex1, vertex2, weight, id):
        e = Edge(id, self._vertices[vertex1], self._vertices[vertex2], weight)
        self._vertices[vertex1].add_edge(e)
        self._vertices[vertex2].add_edge(e)
        self._edges.append(e)

    def print_vertices(self, list_of_vertices=None):
        for v in self._vertices:
            copy = deepcopy(self)
            if list_of_vertices is None or v.id in list_of_vertices:
                print(str(v))
                q = self.enumeration_ask(v.evacuees, copy._evidence_list)
                print("P(Evacuees {} | {}) = {}\n".format(v.id, [(i.get_name() if j else "! " + i.get_name()) for
                                                                 (i, j) in self._evidence_list], q[0]))

    def print_edges(self, list_of_edges=None):
        for edge in self._edges:
            copy = deepcopy(self)
            if list_of_edges is None or edge.id in list_of_edges:
                print(str(edge))
                q = self.enumeration_ask(edge.blockage, copy._evidence_list)
                print("P(Blockage {} | {}) = {}\n".format(edge.id, [(i.get_name() if j else "! " + i.get_name()) for
                                                                 (i, j) in self._evidence_list], q[0]))

        # for edge in self._edges:
        #     if list_of_edges is None or edge.id in list_of_edges:
        #         print(str(edge))

    def path_free_of_blockages(self, list_of_edges=None):

        prob = 1
        for edge in self._edges:
            copy = deepcopy(self)
            if list_of_edges is None or edge.id in list_of_edges:
                q = self.enumeration_ask(edge.blockage, copy._evidence_list)
                prob *= q[1]  # probability that edge.blockage is false
                edge.blockage_reported(False)
                copy._evidence_list.append((edge.blockage, False))
        print("\n------------")
        print("The probability that the given path is free from blockages is {}\n------------".format(prob))

        # copy = deepcopy(self)
        # prob = 1
        # for edge in copy._edges:
        #     if list_of_edges is None or edge.id in list_of_edges:
        #         print("P(! {}) = {}".format(edge.id, P(-edge.blockage)))
        #         prob *= P(-edge.blockage)
        #         edge.blockage_reported(False)
        # print("\n------------")
        # print("The probability that the given path is free from blockages is {}\n------------".format(prob))

        # prob = 0
        # vertices_indices = []

        # for v in self._vertices:
        #     vertices_indices.append(v.id)
        #
        # for perm in list(itertools.product([False, True], repeat=len(vertices_indices))):
        #     temp_prob = 1
        #
        #     for v in self._vertices:
        #         temp_prob *= P(v.flood_p) if perm[vertices_indices.index(v.id)] else P(-v.flood_p)
        #
        #     for edge in self._edges:
        #         if list_of_edges is not None and edge.id in list_of_edges:
        #             flooding_temp = [perm[vertices_indices.index(edge.v1.id)], perm[vertices_indices.index(edge.v2.id)]]
        #             blockage_temp = Blockage(edge.id, edge.weight, flooding_temp, [edge.v1, edge.v2])
        #
        #             temp_prob *= (1 - blockage_temp.noisy_or(flooding_temp))
        #     prob += temp_prob
        #
        # print("\n------------")
        # print("The probability that the given path is free from blockages is {}\n------------".format(prob))



if __name__ == '__main__':
    g = Graph(4)
    print(str(g))
    g.print_vertices()