from graph import *


class BayesNetwork(Graph):
    def __init__(self, num_of_vertices):
        Graph.__init__(self, num_of_vertices)

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
            evidence.append((query_var, query_val))
            q.append(self.enumerate_all(vars, evidence))
        return q / sum(q)

    def enumerate_all(self, vars, evidence):
        if not vars:
            return 1
        Y = vars.pop(0)
        for (Y_var, y_val) in evidence:
            if Y_var.id == Y.id:
                prob = P(Y) if y_val else P(-Y)
                return prob * self.enumerate_all(vars, evidence)
            else:
                sigma = 0
                for y_v in [True, False]:
                    prob = P(Y) if y_v else P(-Y)
                    sigma += prob * self.enumerate_all(vars, evidence.append((Y, y_v)))
                return sigma
