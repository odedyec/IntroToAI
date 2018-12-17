from prob_lib import ProbVar


class Blockage(ProbVar):
    """
    The blockages are noisy-or distributed given the flooding at incident vertices, with pi =(1-qi)= 0.6*1/w(e)
    """
    def __init__(self, edge_id, edge_weight, floodings, vertices):
        ProbVar.__init__(self, 1.)
        self._id = edge_id
        self.vertices = vertices
        self.edge_weight = edge_weight
        self.floodings = floodings
        self.calculate_value()

    def update_floodings(self, floodings):
        """
        A list of two booleans denoting if there is a flood at vertex 1 and vertex 2
        :param floodings:
        """
        self.floodings = floodings
        self.calculate_value()

    def calculate_value(self):
        """
        Calculate the probability value based on the flooding situation
        """
        self.value = 1.
        if None in self.floodings:
            for v, flood in enumerate(self.floodings):
                if flood is None:
                    self.value *= (self.vertices[v].flood_p.value * (self.probability_of_blockage_if(True))
                                   )
                elif flood is True:
                    self.value *= self.probability_of_blockage_if(True)
                else:
                    self.value *= self.probability_of_blockage_if(False)
            self.value = 1 - self.value
            return

        for v, flood in enumerate(self.floodings):
            if flood:
                self.value *= self.probability_of_blockage_if(True)
        self.value = 1. - self.value

    def probability_of_blockage_if(self, what=True):
        return 0.6 * 1 / self.edge_weight if what else 0.

    def __str__(self):
        s = 'P(Blockage {}|'.format(self._id)
        if self.floodings[0] is not None:
            s += '' if self.floodings[0] is True else '!'
            s += 'flood{} '.format(self.vertices[0].id)
        if self.floodings[1] is not None:
            s += '' if self.floodings[1] is True else '!'
            s += 'flood{}'.format(self.vertices[1].id)
        s += ')={}'.format(self.value)
        return s


if __name__ == '__main__':
    class V:
        def __init__(self, flood_p=0., id=1):
            self.flood_p = ProbVar(flood_p)
            self.id = id
    b = Blockage(1, 1, [True, True], [V(id=1), V(id=2)])
    print(str(b))
    b = Blockage(1, 1, [None, None], [V(id=1, flood_p=0.1), V(id=2, flood_p=0.1)])
    print(str(b))