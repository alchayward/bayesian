import graph


def round_1_staging(preseeding):
    """preseeding is a dictionary {rank : team}. rank starts at 1 :("""
    return [(preseeding[i], preseeding[i + 1]) for i in range(1, len(preseeding), 2)]


def round_2_staging(round_1_games):
    """takes in partial or full game results from round 1 and starts seeding round 2
     Assume that games in the first round were staged according to round_1_staging.
     order is important here...
     """
    # This is pretty fragile right now.
    winners, losers = (map(lambda x: x.winner, round_1_games), map(lambda x: x.loser, round_1_games))
    first_game = winners[:2]
    last_game = losers[-2:]
    other_games = map(list, zip(winners[2:], losers[:-2]))

    return [first_game] + other_games + [last_game]


def build_team_graph(games, teams_to_stage):
    g = graph.complete_graph_from_node_list(teams_to_stage)

    g.remove_edges_from(filter(  # remove edges of games already played
        lambda ts: all([t in teams_to_stage for t in ts]),
        map(lambda game: game.teams, games)))
    return g


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


# def stage_round(games, teams, round, trace):
#     pass
