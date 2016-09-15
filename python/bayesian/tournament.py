class Game:

    def __init__(self, teams, scores=None, game_id=None):
        """Game object.
            teams is a list of two teams. identifcation via object id
            scores is a dictionary {team:score}
            """
        self.id = game_id
        self.teams = teams

        if not scores:
            self.completed = False
            self.scores = {zip(teams, [None, None])}
        else:
            self.completed = True
            self.scores = scores


# This function might be superflous at the moment. but I might want to use a more
# sophistcated id tracking thing later
def new_game(team_1, team_2):
    return Game([team_1, team_2])
