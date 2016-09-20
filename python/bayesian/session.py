from models import default_parameters, model_from_parameters
from montecarlo import get_trace_dict
from game import completed


def new_session(ts, preseeding=None, model_parameters=default_parameters):
    return {'teams': ts,
            'rounds': dict(),
            'preseeding': preseeding,
            'proposed_games': [],
            'mc_traces': None,
            'model_params': model_parameters}


def mc_traces_is_current(session):
    return set(session['mc_traces']['games']) == set(completed_games(session))


def find_round(session, game):
    for r in session['rounds']:
        if game in r['games'].values():
            return r
    return None


def games(session):
    return sum(gs for gs in session['rounds'].values())


def teams(session):
    return session['teams']


def completed_games(session):
    return filter(completed, games(session))
