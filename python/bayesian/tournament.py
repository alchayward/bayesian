class Game:

    def __init__(self, teams, scores=[None, None], round=None, id=None):
        self.id = id
        self.teams = teams
        self.scores = {zip(teams,scores)}
        self.round = round;
        if not all(self.scores):
            self.completed = False
        else:
            self.completed = True


def new_game(team_1, team_2, round=None):
    return Game([team_1, team_2], round=round)