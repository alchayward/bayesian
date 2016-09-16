import numpy as np
from numpy.random import poisson


# rewrite kl info function:


def shannon_entropy(prb_dist):
    """computes shannon entropy of prb_dist
        H = sum(p log(p))
        prb_dist is a one dimensional numpy array of probabilities.
    """
    x = prb_dist[prb_dist > 0.0]  # filter out zero values
    return -np.sum(x * np.log(x))


def bin_samples(sample):
    bins = np.array(map(lambda x: np.arange(-0.5, x + 1.5, 1),
                        np.amax(sample, axis=1)))
    hist, _, _ = np.histogram2d(sample[0], sample[1], bins=bins, normed=True)
    return np.ndarray.flatten(hist)


def generate_samples(x, draw_fn, n_samples=1):
    """draw samples from a distribution from each instance of x
        each row of x should contain the paramters of f_draw
        each sample should be an object comparable by == """
    return draw_fn(np.tile(x,n_samples))


def expectation(trace, entropy_fn):
    return np.sum(entropy_fn(trace)) / np.shape(trace)[1]


def kl_info(team_trace, param_trace, draw_fn, entropy_fn):
    """returns the (reduced) kl infomation for a pair of teams needed for staging estimation
    for teams indexed by team_idx = [idx1, idx2], trace[idx1][:]
    should return the strength parameters for team 1 etc. and trace[param][:] the
    function paramters for each sample of P(theta)

    f_draw takes ndarray([theta1, theta2, param1, param2,etc]) and returns ndarray([score1, score2])
    """
    # idx = team_idx + param_idx
    trace = np.concatenate((team_trace, param_trace))
    return shannon_entropy(
        bin_samples(
            generate_samples(
                trace, draw_fn))) \
           + expectation(trace, entropy_fn)


# Poisson stuff

def arctan_rate_fn(x):
    return np.array([x[2] * np.exp(x[3] * np.arctan(x[0] - x[1])),
                     x[2] * np.exp(x[3] * np.arctan(x[1] - x[0]))])


def draw_from_poisson(x, rate_fn):
    return poisson(rate_fn(x)) # this is overkill


def poisson_entropy(l):
    return (1 - np.exp(-np.pi * l ** 2)) * 1.61 * np.power(np.log(1 + l), 0.532) \
           + np.exp(-np.pi * l ** 2) * (l * np.log(np.e / l))


def poisson_entropy_fn(x, rate_fn):
    rate_fn(x)
