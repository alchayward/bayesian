#import sqlalchemy as sql
from tournament import new_tournament
from game import new_game


def new_database():
    return {'tournaments': [], 'players': [], 'games': [], 'teams': [], 'sessions': []}

db_file = 'sqlite:///:memory:'
#engine = sql.create_engine(db, echo=True)


