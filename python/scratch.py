import bayesian.handlers as h
from bayesian.team import new_team
from bayesian.session import new_session, new_round
from bayesian.tournament import new_tournament
from bayesian.database import new_database

db = new_database()

sf = new_tournament('SlayerFestII')

h.add_tournament(db, sf)

team_data = ['t1', 't2', 't3', 't4']
[h.add_team_to_tournament(sf, new_team(tn)) for tn in team_data]

s1 = new_session()


game_data = []




