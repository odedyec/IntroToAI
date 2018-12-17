from prob_lib import ProbVar


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
        self.calculate_value()

    def update_edges(self, edges_weight):
        self.edges_weight = edges_weight
        self.calculate_value()

    def update_blockages(self, blockages):
        self.blockages = blockages
        self.calculate_value()

    def calculate_value(self):
        for edge_weight, blockage in zip(self.edges_weight, self.blockages):
            if blockage is None:
                continue
            if blockage:
                self.value *= 0.8 if edge_weight > 4 else 0.4
        self.value = 1 - self.value

    def print_conditional_prob(self, edges):
        s = "P(Evacuees|"
        for i, p in enumerate(self.blockages):
            s += "Blockage{} ".format(edges[i].id) if p else "!Blockage{} ".format(edges[i].id)
        s += ')={}\n'.format(self.value)
        print s


if __name__ == '__main__':
    e = Evacuees([1], [True])
    print(str(e))
    e = Evacuees([1], [False])
    print(str(e))
    e = Evacuees([1], [True])
    print(str(-e))
    e = Evacuees([1], [False])
    print(str(-e))

    e = Evacuees([1, 8], [True, True])
    print(str(e))