from prob_lib import ProbVar


class Blockage(ProbVar):
    """
    The blockages are noisy-or distributed given the flooding at incident vertices, with pi =(1-qi)= 0.6*1/w(e)
    """
    def __init__(self, edge_weight, floodings):
        ProbVar.__init__(self, 1.)
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
        for flood in self.floodings:
            if flood:
                self.value *= 0.6 * 1 / self.edge_weight
        self.value = 1 - self.value


if __name__ == '__main__':
    b = Blockage(1, [True, False])
    print(str(b))
    b = Blockage(1, [True, True])
    print(str(b))
    b = Blockage(1, [False, True])
    print(str(b))
    b = Blockage(1, [False, False])
    print(str(b))

    b = Blockage(1, [False, False, True, True, False])
    print(str(b))


