class Team:

    def __init__(self):
        pass

    @staticmethod
    def new_team(name, members=None, t_id=None):
        return {'id': t_id, 'name': name, 'members': members}
