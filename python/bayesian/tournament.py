class Game:

    def __init__(self, teams, scores=None, game_id=None):
        self.id = game_id
        self.teams = teams

        if not scores:
            self.completed = False
            self.scores = {zip(teams,[None, None])}
        else:
            self.completed = True
            self.scores = scores


def new_game(team_1, team_2):
    return Game([team_1, team_2])
