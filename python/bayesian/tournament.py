def new_tournament(teams, t_id=None):
    return {'id': t_id, 'teams': teams, 'sessions': []}


def add_team(tournament, team):
    tournament['teams'].append(team)


def add_session(tournament, session):
    tournament['sessions'].append(session)
