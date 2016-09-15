import numpy as np
from numpy.random import poisson

# rewrite kl info function:


def shannon_entropy(prb_dist):
    """computes shannon entropy of prb_dist
        H = sum(p log(p))
        prb_dist is a one dimensional numpy array of probabilities.
    """
    x = prb_dist[prb_dist > 0.0]  # filter out zero values
    return -np.sum(x*np.log(x))


def bin_samples(sample):
    bins = np.amax(sample, axis=0)  # number of bins in each dim
    # noinspection PyCallByClass
    return np.ndarray.flatten(np.histogramdd(sample, bins=bins, normed=True))


def generate_samples(x, f_draw, n_samples=1):
    # type: (np.ndarray, (np.ndarray -> np.ndarray, int) -> np.ndarray
    """draw samples from a distribution from each instance of x
        each row of x should contain the paramters of f_draw
        each sample should be an object comparable by == """
    return np.ndarray(sum([map(f_draw, x) for i in range(n_samples)]))
    # Gotta check that f_draw will be changing each time I hit it.


def expectation(trace, entropy_fn):
    return sum(entropy_fn(trace))/len(trace)


def kl_info(trace, draw_fn, entropy_fn, team_idx, param_idx):
    """returns the (reduced) kl infomation for a pair of teams needed for staging estimation
    for teams indexed by team_idx = [idx1, idx2], trace[idx1][:]
    should return the strength parameters for team 1 etc. and trace[param][:] the
    function paramters for each sample of P(theta)

    f_draw takes ndarray([theta1, theta2, param1, param2,etc]) and returns ndarray([score1, score2])
    """
    idx = team_idx + param_idx

    return shannon_entropy(
             bin_samples(
               generate_samples(
                trace[idx][:], draw_fn))) + expectation(trace[idx][:], entropy_fn)



def draw_from_possion(x, rate_fn):
    return np.ndarray(map(poisson, rate_fn(x)))

