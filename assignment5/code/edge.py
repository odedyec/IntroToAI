from prob_lib import ProbVar
class Edge:
    """
    Edge object - connects between v1 and v2 with weight.
    The ID is as given in the input graph (e.g. #E1 - 1 is the ID)
    Also already contains a blockage object
    """
    def __init__(self, id, v1, v2, weight, blockage_p):
        self.v1 = v1
        self.v2 = v2
        self.id = id
        self.weight = weight
        self.blockage = ProbVar(blockage_p)

    def set_blockage_prob(self, p):
        self.blockage = ProbVar(p)

    def blockage_reported(self, what=True):
        self.blockage.value = 1.0 if what else 0.
