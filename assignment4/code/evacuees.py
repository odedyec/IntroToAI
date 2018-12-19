from prob_lib import *


class Evacuees(ProbVar):
    """
    The probability of evacuees at vertex based on edges weights and the blockages

    There are people at vertex v, with noisy or distributions given all the edge blockages at all edges incident on v,
    with pi = 0.8 for an edge with weight greater then 4, and with pi=0.4 for shorter edges..
    """
    def __init__(self, edges_weight, blockages):
        """
        :param edges_weight: a list of edges connected to the vertex
        :param blockages:    a list of booleans denoting the blockage status. Has to be same size as edges list
        """
        ProbVar.__init__(self, 1.)
        self.edges_weight = edges_weight
        self.blockages = blockages
        self._evacuees_reported = None
        self.calculate_value()

    def report(self, what):
        self._evacuees_reported = what
        self.calculate_value()

    def update_edges(self, edges_weight):
        self.edges_weight = edges_weight
        self.calculate_value()

    def update_blockages(self, blockages):
        self.blockages = blockages
        self.calculate_value()

    def calculate_value(self):
        if self._evacuees_reported is True:
            self.value = 1.0
            return
        if self._evacuees_reported is False:
            self.value = 0.
            return

        conditions = []
        for blockage in self.blockages:
            conditions.append((P(-blockage), P(blockage)))
        self.value = total_probability(self.noisy_or, conditions)

    def noisy_or(self, conditions):
        if len(list(filter(lambda condition: condition is True, conditions))) == 0:
            return 0.001
        value = 1.0
        for edge_weight, condition in zip(self.edges_weight, conditions):
            if condition:
                value *= 0.8 if edge_weight > 4 else 0.4
        return 1.0 - value

    def print_conditional_prob(self, edges):
        s = "P(Evacuees|"
        for i, p in enumerate(self.blockages):
            s += "Blockage{} ".format(edges[i].id) if p else "!Blockage{} ".format(edges[i].id)
        s += ')={}\n'.format(self.value)
        print (s)

