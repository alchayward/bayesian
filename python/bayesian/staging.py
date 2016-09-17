import tournament
import networkx as nx


def round_1_staging(preseeding):
    """preseeding is a dictionary {rank : team}. rank starts at 1 :("""
    return [[preseeding[i], preseeding[i+1]] for i in range(1, len(preseeding), 2)]


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


def build_kl_graph(games, teams_to_stage, teams_trace, param_trace):
    pass
    # get complete graph from nodes with teams to stage
    G = nx.complete_graph(teams_to_stage)
    # remove edges of games already played
    G.remove_edges_from(filter(
        lambda ts: all([t in teams_to_stage for t in ts]),
        map(lambda g: g.teams, games)))
    # compute kl_info for each edge. Something special for instamix team

    # return graph with weighted edges


def stage_games_bayesian(games, teams_to_stage, teams_trace, param_trace):
    kl_graph = build_kl_graph(games, teams_to_stage, teams_trace, param_trace)
    return nx.max_weight_matching(kl_graph)

def stage_round(games, teams, round, trace):
    pass



