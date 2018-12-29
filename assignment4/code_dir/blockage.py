from prob_lib import *


class Blockage(ProbVar):
    """
    The blockages are noisy-or distributed given the flooding at incident vertices, with pi =(1-qi)= 0.6*1/w(e)
    """
    def __init__(self, edge_id, edge_weight, floodings, vertices, report=None):
        ProbVar.__init__(self, 1., "Blockage " + str(edge_id))
        self._id = edge_id
        self.vertices = vertices
        self.edge_weight = edge_weight
        self.floodings = floodings
        self._blockage_reported = report
        self.calculate_value()

    def is_blockage_reported(self):
        return self._blockage_reported

    def report(self, what):
        self._blockage_reported = what
        for vertex in self.vertices:
            vertex.blockage_reported()
        self.calculate_value()

    def update_floodings(self, floodings):
        """
        A list of two booleans denoting if there is a flood at vertex 1 and vertex 2
        :param floodings:
        """
        self.floodings = floodings
        self.calculate_value()
        for vertex in self.vertices:
            vertex.blockage_reported()

    def calc_prob_from_evidence(self, evidence=None):
        if evidence is None:
            evidence = []
        parents = [None, None]
        for (var, val) in evidence:
            for i in [0, 1]:
                if var.get_name() == self.vertices[i].flood_p.get_name():
                    parents[i] = val
        return self.noisy_or(parents)



    def calculate_value(self):
        """
        Calculate the probability value based on the flooding situation
        """
        if self._blockage_reported is True:
            self.value = 1.
            return
        if self._blockage_reported is False:
            self.value = 0.
            return
        self.value = 0.
        prob_conditions = []
        for v, flood in enumerate(self.floodings):
            if flood is None:
                p_true, p_false = P(self.vertices[v].flood_p), P(-self.vertices[v].flood_p)
            else:
                (p_true, p_false) = (1.0, 0.0) if flood is True else (0.0, 1.0)
            prob_conditions.append((p_false, p_true))
        self.value = total_probability(self.noisy_or, prob_conditions)

    def noisy_or(self, conditions):
        """
            This function is a noisy-or implementation
            P(x | condtions) = 1 - PI_{if condition is true}( Value if true)

            :param value_if_true: The value if true
            :param list_conditions:  a list of booleans
            :return: Noisy-Or probability
            """
        p = 0.6 * 1 / self.edge_weight
        if conditions[0] and conditions[1]: return 1 - (1 - p) * (1 - p)
        if not conditions[0] and not conditions[1]: return 0.001
        return p
        #
        # l = list(filter(lambda x: x is True, conditions))
        # return 1 - self.probability_of_blockage_if(True) ** len(l)

    def probability_of_blockage_if(self, what=True):
        return 0.6 * 1 / self.edge_weight if what else 0.001

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

#
# if __name__ == '__main__':
#     class V:
#         def __init__(self, flood_p=0., id=1):
#             self.flood_p = ProbVar(flood_p)
#             self.id = id
#     b = Blockage(1, 1, [True, True], [V(id=1), V(id=2)])
#     print(str(b))
#     b = Blockage(1, 1, [None, None], [V(id=1, flood_p=1.), V(id=2, flood_p=0.1)])
#     print(str(b))