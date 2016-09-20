from session import find_round, games
from game import completed
from models import model_from_parameters
from montecarlo import get_trace_dict

def get_item_id(ind_dict):
    # Check if it's in there first?
    ids = ind_dict.keys()
    if len(ids) == 0:
        m_id = 0
    else:
        m_id = max(ind_dict.keys()) + 1
    return m_id


def add_team_to_session(db, session_id, team_id):
    db['sessions'][session_id]['teams'].append(team_id)


def remove_game_from_session(db, session_id, game_id):
    # find which round the game is in
    sess = db['sessions'][session_id]
    r = find_round(sess, game_id)
    r['games'].remove(game_id)


def add_round_to_session(db, session_id, rnd):
    db['sessions'][session_id]['rounds'].update({rnd: []})


def add_game_to_round(db, session_id, rnd, game_id):
    db['sessions'][session_id]['rounds'][rnd].append(game_id)


def add_team_to_tournament(db, tournament_id, team_id):
    db['tournaments'][tournament_id]['teams'].append(team_id)


def add_session_to_tournament(db, tournament_id, session_id):
    db['tournaments'][tournament_id]['sessions'].append(session_id)


def update_mc_traces(db, session_id, all_games=None):
    sess = db['sessions'][session_id]
    if all_games is None:
        all_games = games(sess)
    gs = [db['games'][g] for g in filter(completed, all_games)]
    model = model_from_parameters(sess['model_params'])
    sess['mc_traces'] = {'trace_dict': get_trace_dict(model, sess['teams'], all_games),
                            'games': gs}



def new_thing(db, collection, t):
    c_id = get_item_id(db[collection])
    db[collection].update({c_id: t})
    return c_id


def new_tournament(db, t):
    return new_thing(db, 'tournaments', t)


def new_session(db, s):
    return new_thing(db, 'sessions', s)


def new_team(db, t):
    return new_thing(db, 'teams', t)


def new_game(db, g):
    return new_thing(db, 'games', g)
