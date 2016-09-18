import numpy as np
from numpy import log


def shannon_entropy(prb_dist):
    """computes shannon entropy of prb_dist
        H = sum(p log(p))
        prb_dist is a one dimensional numpy array of probabilities.
    """
    return (lambda x: -np.sum(x * log(x)))(prb_dist[prb_dist > 0.0])


def bin_samples(sample):
    return np.ndarray.flatten(
        np.histogram2d(
            sample[:, 0], sample[:, 1],
            bins=map(lambda x: np.arange(-0.5, x + 1.5, 1), np.amax(sample, axis=0)),
            normed=True)[0])


def generate_samples(x, draw_fn, n_samples=1):
    """draw samples from a distribution from each instance of x
        each row of x should contain the paramters of f_draw
        each sample should be an object comparable by == """
    # noinspection PyTypeChecker
    return draw_fn(np.tile(x, (n_samples, 1)))  # creates a larger intermediate array. could do iteratively


def expectation(trace, fn):
    return np.sum(fn(trace), axis=0) / (1.0 * trace.shape[0])  # will return a vector. so be careful


def kl_info(team_trace, param_trace, draw_fn, entropy_fn):
    """returns the (reduced) kl infomation for a pair of teams needed for staging estimation
    for teams indexed by team_idx = [idx1, idx2], trace[idx1][:]
    should return the strength parameters for team 1 etc. and trace[param][:] the
    function paramters for each sample of P(theta)

    f_draw takes ndarray([theta1, theta2, param1, param2,etc]) and returns ndarray([score1, score2])
    """
    trace = np.concatenate((team_trace, param_trace), axis=1)
    return shannon_entropy(bin_samples(generate_samples(trace, draw_fn))) \
           + np.sum(expectation(trace, entropy_fn))


