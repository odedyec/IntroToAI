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
        self.blockage = Blockage(self.id, weight, [None, None], [v1, v2])

    def print_prob_for_blockage(self):
        print(str(self.blockage))

    def __str__(self):
        s = 'Edge{}\n'.format(self.id)
        s += '----------\n'
        s += '{}\n'.format(Blockage(self.id, self.weight, [False, False],[self.v1, self.v2]))
        s += '{}\n'.format(Blockage(self.id, self.weight, [False, True],[self.v1, self.v2]))
        s += '{}\n'.format(Blockage(self.id, self.weight, [True, False],[self.v1, self.v2]))
        s += '{}\n'.format(Blockage(self.id, self.weight, [True, True],[self.v1, self.v2]))

        return s

    def reset(self):
        self.blockage.update_floodings([None, None])
