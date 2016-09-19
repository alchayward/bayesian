import graph
from models import default_parameters


def new_session(team_ids, preseeding=None, model_parameters=default_parameters):
    return {'teams': team_ids,
            'games': [],
            'rounds': dict(),
            'preseeding': preseeding,
            'model_params': model_parameters}


def add_game_to_session(session, game_id, rnd):
    sess = session.copy()
    sess['games'] = session['games'] + [game_id]
    try:
        sess['rounds'][rnd].append(game_id)
    except KeyError:
        sess['rounds'].update({rnd, [game_id]})
    return sess


def round_1_staging(preseeding):
    """preseeding is a dictionary {rank : team}. rank starts at 1 :("""
    return [[preseeding[i], preseeding[i + 1]] for i in range(1, len(preseeding), 2)]


def round_2_staging(round_1_games, win_fn, lose_fn):
    """takes in partial or full game results from round 1 and starts seeding round 2
     Assume that games in the first round were staged according to round_1_staging.
     order is important here...
     win_fn, lose_fn need to return the winner/loser from a game or None if it hasn't been played.
     In the case of a draw they need to pick one of them out
     """
    winners, losers = (map(lambda x: win_fn(x), round_1_games),
                       map(lambda x: lose_fn(x), round_1_games))
    first_game = winners[:2]
    last_game = losers[-2:]
    other_games = map(list, zip(winners[2:], losers[:-2]))
    games = [first_game] + other_games + [last_game]
    return filter(lambda g: any([t is None for t in g]), games)


def build_team_graph(games, teams_to_stage):
    g = graph.complete_graph_from_node_list(teams_to_stage)

    g.remove_edges_from(filter(  # remove edges of games already played
        lambda ts: all([t in teams_to_stage for t in ts]),
        map(lambda game: game.teams, games)))
    return g

# Need to put this insta-mix logic somewhere
# if any(getattr(t, 'is_instamix', False) for t in e):  # test for instamix team
#     g[e]['weight'] = 0
# else:  # compute kl information
#     g[e]['weight'] = kl_info(
#         model_data['teams_trace'][:, map(lambda t: model_data['team_index'][t], e)],
#         model_data['param_trace'],
#         model_data['draw_fn'], model_data['entropy_fn'])


def stage_games_bayesian(games, teams_to_stage, weight_fn):
    return graph.games_from_weighted_graph(
        graph.add_weights_to_graph(
            build_team_graph(games, teams_to_stage),
            weight_fn))
