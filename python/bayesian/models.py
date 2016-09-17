# Poisson stuff
import numpy as np
from numpy.random import poisson
from scipy.special import gammaln
from numpy import log, exp, arctan
import pymc


def model_dict(log_prob, draw_fn, entropy_fn, param_priors):
    return {'log_prob': log_prob,
            'draw_fn': draw_fn,
            'entropy_fn': entropy_fn,
            'param_priors': param_priors}


def poission_model(rate_fn, param_priors):
    return model_dict(lambda x,k: log_poisson_pr(rate_fn(x), k),
                      )


def arctan_rate_fn(x):
    return np.transpose(np.array([x[:, 2] * exp(x[:, 3] * arctan(x[:, 0] - x[:, 1])),
                     x[:, 2] * exp(x[:, 3] * arctan(x[:, 1] - x[:, 0]))]))


def log_poisson_pr(l, k):
    return k * log(l) - l - gammaln(k + 1)


def draw_from_poisson(x, rate_fn):
    return poisson(rate_fn(x))  # this is overkill


def poisson_entropy(l):
    """This is an approximate expression for the entropy. Need to work out something better
    at some point"""
    # noinspection PyTypeChecker
    return (1 - exp(-np.pi * l ** 2)) * 1.61 * np.power(log(1 + l), 0.532) \
           + exp(-np.pi * l ** 2) * (l * log(np.e / l))
