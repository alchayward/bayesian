class Game:

    def __init__(self, teams, scores=None, game_id=None):
        """Game object.
            teams is a list of two teams. identifcation via object id
            scores is a dictionary {team:score}
            """
        self.id = game_id
        self.teams = teams

    @staticmethod
    def new_game(teams, scores=None):

        if not scores:
            scores = dict(zip(teams, [None, None]))
        return {'teams': teams, 'scores': scores}

    @staticmethod
    def scores(g):
        return g['scores']

    @staticmethod
    def teams(g):
        return g['teams']

    @staticmethod
    def completed(g):
        return all(g['scores'].values())

    @staticmethod
    def winner(g):  # not sure what to put here in case of draw
        if Game.completed(g):
            scores = Game.scores(g)
            teams = Game.teams(g)
            if scores[teams[0]] > scores[teams[1]]:
                return teams[0]
            else:
                return teams[1]
        else:
            return None

    @staticmethod
    def loser(g):  # not sure what to put here in case of draw

        if Game.completed(g):
            scores = Game.scores(g)
            teams = Game.teams(g)
            if scores[teams[0]] > scores[teams[1]]:
                return teams[1]
            else:
                return teams[0]
        else:
            return None

    @staticmethod
    def is_draw(g):
        if Game.completed(g):
            scores = Game.scores(g)
            teams = Game.teams(g)
            if scores[teams[0]] == scores[teams[1]]:
                return True
            else:
                return False
        else:
            return None
