import tournament


def round_1_staging(preseeding):
    """preseeding is a dictionary {rank : team}"""
    return [[preseeding[i],preseeding[i+1]] for i in range(1, len(preseeding), 2)]


def round_2_staging(games):
    """takes in partial or full game results from round 1 and starts seeding round 2
     Assume that games in the first round were staged according to round_1_staging
     """

