from session import find_round, completed_games
from models import model_from_parameters
from montecarlo import get_trace_dict


def add_team_to_session(session, team):
    session['teams'].append(team)


def remove_game_from_session(session, game):
    # find which round the game is in
    r = find_round(session, game)
    r['games'].remove(game)


def add_round_to_session(session, rnd):
    session['rounds'].append(rnd)


def add_game_to_round(rnd, game):
    rnd['games'].append(game)


def add_team_to_tournament(tournament, team):
    tournament['teams'].append(team)


def add_session(tournament, session):
    tournament['sessions'].append(session)


def update_mc_traces(session, all_games=None):
    gs = completed_games(session)
    if all_games is None:
        all_games = gs
    model = model_from_parameters(session['model_params'])
    session['mc_traces'] = {'trace_dict': get_trace_dict(model, session['teams'], all_games),
                            'games': gs}


def add_tournament(db, t):
    db['tournaments'].append(t)
