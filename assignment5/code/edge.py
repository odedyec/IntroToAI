from prob_lib import ProbVar, P

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
        self._is_blocked = self.blockage.draw_boolean()

    def set_blockage_from_knowledge(self):
        self.set_blockage_prob(1.) if self._is_blocked else self.set_blockage_prob(0.)

    def set_blockage_prob(self, p):
        self.blockage = ProbVar(p)

    def blockage_reported(self, what=True):
        self.blockage.value = 1.0 if what else 0.

    def blockage_unclear(self):
        if P(self.blockage) == 0. or P(self.blockage) == 1.:
            return False
        return True

    def __str__(self):
        if P(self.blockage) == 0.:
            return "E{}_b".format(self.id)
        if P(self.blockage) == 1.:
            return "E{}_c".format(self.id)
        return "E{}_u".format(self.id)