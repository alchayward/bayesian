# ways for scoring based off results
import numpy as np
from prob import expectation


def wld(games):
    pass


def most_likely_ordering(games):
    pass


def average_strength(strength_trace):
    return expectation(strength_trace, lambda x: x)


def ordering(strengths):
    return np.argsort(strengths, axis=1) + 1


def average_ordering(strength_trace):
    return expectation(strength_trace, ordering)
