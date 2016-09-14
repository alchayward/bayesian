import numpy as np
from numpy.random import poisson

# rewrite kl info function:


def shannon_entropy(prb_dist):
    """computes shannon entropy of prb_dist
        H = sum(p log(p))
        prb_dist is a one dimensional numpy array of probabilities.
    """
    x = prb_dist[ prb_dist > 0.0] #filter out zero values
    return -np.sum(x*np.log(x))


def bin_samples(sample):
    bins = [max(x) for x in sample] #number of bins in each dim
    return np.ndarray.flatten(np.histogramdd(sample, bins=bins, normed=True))


def generate_samples(x, f_draw, n_samples=1):
    """draw samples from a distribution from each instance of x
        each row of x should contain the paramters of f_draw
        each sample should be an object comparable by == """
    return np.ndarray(sum([map(f_draw, x) for i in range(n_samples)]))
    # Gotta check that f_draw will be changing each time I hit it.


def draw_from_possion(x, rate_fn):
    return np.ndarray(map(np.random.poisson,rate_fn(x)))


def kl_info(trace, f_draw, team_inds, param_inds):
    inds = team_inds + param_inds
    return shannon_entropy(
            bin_samples(
                generate_samples(
                    trace[inds][:],f_draw))))
