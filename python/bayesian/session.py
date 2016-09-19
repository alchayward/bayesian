from models import default_parameters, model_from_parameters
from montecarlo import get_trace_dict
from game import completed


def new_session(ts, preseeding=None, model_parameters=default_parameters):
    return {'teams': ts,
            'rounds': [],
            'preseeding': preseeding,
            'proposed_games': [],
            'mc_traces': None,
            'model_params': model_parameters}


def mc_traces_is_current(session):
    return set(session['mc_traces']['games']) == set(completed_games(session))


def update_mc_traces(session, all_games=None):
    gs = completed_games(session)
    if all_games is None:
        all_games = gs
    model = model_from_parameters(session['model_params'])
    session['mc_traces'] = {'trace_dict': get_trace_dict(model, session['teams'], all_games),
                            'games': gs}


def new_round(rnd):
    return {'round': rnd, 'games': []}


def add_round_to_session(session, rnd):
    session['rounds'].append(rnd)


def add_game_to_round(rnd, game):
    rnd['games'].append(game)


def find_round(session, game):
    for r in session['rounds']:
        if game in r['games']:
            return r
    return None


def remove_game_from_session(session, game):
    # find which round the game is in
    r = find_round(session, game)
    r['games'].remove(game)


def games(session):
    return sum(r['games'] for r in session['rounds'])


def teams(session):
    return session['teams']


def add_team_to_session(session, team):
    session['teams'].append(team)


def completed_games(session):
    return filter(completed, games(session))
