import pymc
from game import Game
import numpy as np
from scipy import rand


def llh_fn(team_idx, games, prob_fn):
    # list of lists of the form [t1_idx, t2_idx, s1, s2] for each game
    game_list = [[team_idx[Game.teams(g)[0]],
                  team_idx[Game.teams(g)[1]],
                  Game.scores(g)[Game.teams(g)[0]],
                  Game.scores(g)[Game.teams(g)[1]]
                  ] for g in games]

    def log_likelyhood(th, p):
        return sum([prob_fn(th[gv[0]], th[gv[1]], gv[2], gv[3], p) for gv in game_list])
    return log_likelyhood


def make_team_idx(teams):
    return dict(zip(teams, range(len(teams))))


def pymc_model(model, teams, games):
    """

    :param model: dictionary.
        prob_fn: f(t1, t2, score1, score2, parameters). should broadcast...
        params: parameters for log fn. values or pymc variables
    :param teams: list of teams. teams are hashable
    :param games: list of games, that impliment Game functions
    :return: pymc model
    """
    team_idx = make_team_idx(teams)
    log_likelihood = llh_fn(team_idx, filter(lambda g: Game.completed(g), games), model['prob_fn'])
    theta_i = pymc.Normal('theta_i', mu=0, tau=np.power(1/3.0,2), value=rand(len(teams)) * 0.00001)

    @pymc.deterministic()
    def theta(th=theta_i):
        return th - np.mean(th)

    # This feels like the wrong thing to do, but it works. Need to figure out why
    params = model['params'].values()
    n_params = len(params)
    x = np.empty(n_params, dtype=object)
    for i in range(0, n_params):
        x[i] = params[i]()

    @pymc.stochastic(observed=True)
    def games_played(value=np.array([0]), th=theta, p=x):
        return log_likelihood(th, p)

    z = locals().copy()
    # z.update(model['params'].keys())
    m = pymc.Model(z)

    for key in m.__dict__.keys():  # seems to need this or ot throws an error
        if not isinstance(key, basestring):
            del m.__dict__[key]
    return m


def mcmc_fit(mc_model, mcmc_parameters):
    """takes in a pymc model, and some mcmc parameters and returns a mcmc chain"""
    mcmc = pymc.MCMC(mc_model)
    mcmc.use_step_method(pymc.AdaptiveMetropolis, mcmc.theta_i)
    print('running MCMC')
    mcmc.sample(mcmc_parameters['points'], mcmc_parameters['burn'], mcmc_parameters['steps'],
                     progress_bar=True)
    print('finished MCMC')
    return mcmc


def maximum_likelyhood_estimate(mc_model):
    """returns the MLE of team strengths and paramter values"""
    m = pymc.MAP(mc_model)
    m.fit()
    return (m.values['theta'],) + tuple(m.values[p] for p in m.params)

    # return team_val, param_val


def mcmc_fit_traces(model, mcmc):
    team_trace = mcmc.trace('theta')[:]
    param_trace = np.array([mcmc.trace(name)[:] for name in model['params'].keys()])
    return team_trace, param_trace
