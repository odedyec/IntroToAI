"""
This file should contain probability library auxiliary functions and objects
"""
import itertools


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


P = lambda probvar: probvar.value


def total_probability(conditional_prob_func, list_of_noisy_boolean_variables):
    """
    A total probability function. Should get the table of probability given conditions, P(X | A,B,C...).
    The table should actually be a function that gets a list of True/False values, namely the conditions
    :param conditional_prob_func:
    :param list_of_noisy_boolean_variables: a list of Probability with tuple <Probability for False,
                                                                              Probability for True>
    :return: The total probability value
    """
    value = 0.
    for perm in list(itertools.product([False, True], repeat=len(list_of_noisy_boolean_variables))):
        idx = map(int, perm)
        prior_prob = 1.0
        for bool_var, idx in zip(list_of_noisy_boolean_variables, idx):
            prior_prob *= bool_var[idx]
        value += conditional_prob_func(perm) * prior_prob
    return value


if __name__ == "__main__":
    v = ProbVar(0.4)
    v2 = ProbVar(0.4)
    print (P(v2))
    print (str(v))
    print (str(-v))
    print (str(v+v2))
    print (str(v * v2))
    print (str(v.p_or(v2)))

    def my_noisy_or(list_of_conditions):
        return noisy_or(0.6, list_of_conditions)
    print (total_probability(my_noisy_or, [(0., 1), (1., 0.)]))