# Poisson stuff
import numpy as np
from numpy.random import poisson
from scipy.special import gammaln
from numpy import log, exp, arctan
from pymc.distributions import TruncatedNormal


default_mc_parameters = {'points': 200000, 'burn': 10000, 'steps': 4}

def model_dict(log_prob, draw_fn, entropy_fn, param_priors, mc_params=default_mc_parameters):
    return {'prob_fn': log_prob,
            'draw_fn': draw_fn,
            'entropy_fn': entropy_fn,
            'params': param_priors}


def poisson_model(rate_fn, params):
    return model_dict(
        lambda x1, x2, s1, s2, p:
        (lambda r: log_poisson_pr(r[:, 0], s1) + log_poisson_pr(r[:, 1], s2))(rate_fn(x1, x2, p)),
        lambda x: poisson(rate_fn(x[:, 0], x[:, 1], x[:, 2:])),
        lambda x: np.sum(poisson_entropy(rate_fn(x[:, 0], x[:, 1], x[:, 2:])), axis=1),
        params)


def arctan_poisson_model():
    return poisson_model(arctan_rate_fn,
                   {'scale': lambda: TruncatedNormal('scale', mu=2, tau=np.power(1 / 5.0, 2), value=2, a=0, b=10),
                    'expo': lambda: TruncatedNormal('expo', mu=1, tau=np.power(1 / 5.0, 2), value=1, a=0, b=4)})


def arctan_rate_fn(x1, x2, p):
    d = p[1] * arctan(x1 - x2)
    return np.array([p[0] * exp(d), p[0] * exp(-d)])


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


def default_parameters():
    return {'model': 'arctan'}


def model_from_parameters(parameters):
    return {'arctan': arctan_poisson_model}[parameters['model']]()
