class Game:

    def __init__(self, teams, scores=[None, None], game_id=None):
        self.id = game_id
        self.teams = teams
        self.scores = {zip(teams, scores)}
        if not all(self.scores):
            self.completed = False
        else:
            self.completed = True


def new_game(team_1, team_2):
    return Game([team_1, team_2])
