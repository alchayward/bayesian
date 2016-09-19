import sqlalchemy as sql
from tournament import new_tournament
from game import new_game




db_file = 'sqlite:///:memory:'
engine = sql.create_engine(db, echo=True)


def add_game(game):
    return

def create_database():
    pass


def create_tournament(teams):
    t = new_tournament(teams)

    return t


def update_tournament(tournament):
    pass
