from models import default_parameters
from game import new_game


def new_session(teams, preseeding=None, model_parameters=default_parameters):
    return {'teams': teams,
            'rounds': [],
            'preseeding': preseeding,
            'proposed_games': [],
            'mc_traces': None,
            'model_params': model_parameters}


def get_mc_traces(session):
    # What if we want to use a wider set of games, which we've used in the past?


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
