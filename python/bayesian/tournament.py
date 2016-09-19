def new_tournament(teams, t_id=None):
    return {'id': t_id, 'teams': teams, 'sessions': []}


def add_new_session(tournament, session):
    tournament['sessions'].append(session)
