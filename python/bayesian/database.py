#import sqlalchemy as sql
from tournament import new_tournament
from game import new_game
from pyReframe import Reframe
from pyrsistent import pmap

import dataset

db = dataset.connect('sqlite:///:memory:')

table = db['sometable']
table.insert(dict(name='John Doe', age=37))
table.insert(dict(name='Jane Doe', age=34, gender='female'))

john = table.find_one(name='John Doe')



def new_database():
    return pmap({'tournaments': [], 'players': [], 'games': [], 'teams': [], 'sessions': [], 'db_update'})

R = Reframe(new_database())

def load_database_handler(_, event):
    connection = event[1]
    db = connection.load_all()
    return sql_db_to_python(db)

R.reg_handler('load_db', [], load_database_handler)

db_file = 'sqlite:///:memory:'
#engine = sql.create_engine(db, echo=True)


