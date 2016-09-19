def new_tournament():
    return {'teams': [], 'sessions': []}


def add_team(tournament, team):
    tournament['teams'].append(team)


def add_session(tournament, session):
    tournament['sessions'].append(session)
