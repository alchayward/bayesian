# Do I really need classes. I hate classes. Maybe I should just stick with dicts.
# Problem is that you cant hash a dict....


class Team:

    def __init__(self):
        pass


class Game:

    def __init__(self, teams, scores=None, game_id=None):
        """Game object.
            teams is a list of two teams. identifcation via object id
            scores is a dictionary {team:score}
            """
        self.id = game_id
        self.teams = teams

        if not scores:
            self.scores = dict(zip(teams, [None, None]))
        else:
            self.scores = scores

    @property
    def completed(self):
        return all(self.scores.values())

    @property
    def winner(self):  # not sure what to put here in case of draw
        if self.completed:
            if self.scores[self.teams[0]] > self.scores[self.teams[1]]:
                return self.teams[0]
            else:
                return self.teams[1]
        else:
            return None

    @property
    def loser(self):  # not sure what to put here in case of draw
        if self.completed:
            if self.scores[self.teams[0]] > self.scores[self.teams[1]]:
                return self.teams[1]
            else:
                return self.teams[0]
        else:
            return None

    @property
    def is_draw(self):
        if self.completed:
            if self.scores[self.teams[0]] == self.scores[self.teams[1]]:
                return True
            else:
                return False
        else:
            return None


# This function might be superflous at the moment. but I might want to use a more
# sophistcated id tracking thing later
def new_game(team_1, team_2):
    return Game([team_1, team_2])
