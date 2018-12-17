"""
This file should contain probability library auxiliary functions and objects
"""


class ProbVar:
    """
    A probability object with sigma-algebra properties (value between 0-1, -value == 1 - value
    OR and AND functions are implemented
    """
    def __init__(self, value):
        self.value = value

    def __neg__(self):
        v = ProbVar(1 - self.value)
        return v

    def __sub__(self, other):
        v = ProbVar(max(self.value - other.value, 0))
        return v

    def __add__(self, other):
        v = ProbVar(min(self.value + other.value, 1))
        return v

    def __str__(self):
        return "{}%".format(100 * self.value)

    def __mul__(self, other):
        v = ProbVar(self.value * other.value)
        return v

    def p_and(self, other):
        """
        Calculates the P(self ^ other) probability
        :param other: ProbVar object
        :return:
        """
        return self * other

    def p_or(self, other):
        """
        Calculates the P(self V other) probability
        :param other: ProbVar object
        :return:
        """
        return self + other - self * other


if __name__ == "__main__":
    v = ProbVar(0.4)
    v2 = ProbVar(0.4)
    print str(v)
    print str(-v)
    print str(v+v2)
    print str(v * v2)
    print str(v.p_or(v2))
