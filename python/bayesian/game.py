from useful import flatten


def new_game(ts, ss=None):
    if not ss:
        ss = dict(zip(ts, [None, None]))
    return {'teams': ts, 'scores': ss}


def scores(g):
    return g['scores']


def teams(g):
    return g['teams']


def completed(g):
    return all(g['scores'].values())


def winner(g):  # not sure what to put here in case of draw
    if completed(g):
        s = scores(g)
        t = teams(g)
        if s[t[0]] > s[t[1]]:
            return t[0]
        else:
            return t[1]
    else:
        return None


def loser(g):  # not sure what to put here in case of draw

    if completed(g):
        s = scores(g)
        t = teams(g)
        if s[t[0]] > s[t[1]]:
            return t[1]
        else:
            return t[0]
    else:
        return None


def is_draw(g):
    if completed(g):
        s = scores(g)
        t = teams(g)
        if s[t[0]] == s[t[1]]:
            return True
        else:
            return False
    else:
        return None


def teams_in_games(games):
    return list(set(flatten([g['teams'] for g in games])))
