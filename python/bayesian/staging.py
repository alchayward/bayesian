import tournament


def round_1_staging(preseeding):
    """preseeding is a dictionary {rank : team}"""
    return map(tournament.new_game,
               [[preseeding[i],preseeding[i+1]] for i in range(1, len(preseeding), 2)])
