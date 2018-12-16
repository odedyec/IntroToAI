from blockage import Blockage
import itertools


class Edge:
    """
    Edge object - connects between v1 and v2 with weight.
    The ID is as given in the input graph (e.g. #E1 - 1 is the ID)
    Also already contains a blockage object
    """
    def __init__(self, id, v1, v2, weight):
        self.v1 = v1
        self.v2 = v2
        self.id = id
        self.weight = weight
        self.blockage = Blockage(weight, [False, False])

    def __str__(self):
        s = 'Edge{}\n'.format(self.id)
        s += '----------\n'
        s += 'P(Blockage {}| !flood{}, !flood{})={}\n'.format(self.id, self.v1.id, self.v2.id,
                                                              Blockage(self.weight, [False, False]))
        s += 'P(Blockage {}| !flood{}, flood{})={}\n'.format(self.id, self.v1.id, self.v2.id,
                                                            Blockage(self.weight, [False, True]))
        s += 'P(Blockage {}| flood{}, !flood{})={}\n'.format(self.id, self.v1.id, self.v2.id,
                                                            Blockage(self.weight, [True, False]))
        s += 'P(Blockage {}| flood{}, flood{})={}\n'.format(self.id, self.v1.id, self.v2.id,
                                                            Blockage(self.weight, [True, True]))
        return s

