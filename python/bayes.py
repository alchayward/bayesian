import ranking
import time
import os
from tournament import Team, Game


def make_teams(team_ids):

    def new_team(id,ind):
        t = Team()
        t.id = id
        t.session_id = ind
        return t
    
    return [new_team(ind,id) for ind,id in enumerate(team_ids)]


def mcmc_games(games,teams):
    
    def new_game(id):
        g = Game()
        g.id = game['id']
        g.teams = [game['team_1'],game['team_2']]
        if not game['status'] == 1:
            g.scores = None
        else:
            g.scores = [game['score_1'],game['score_2']]
        g.round = game['round']
        return g
    
    return [new_game(g) for g in games]

def init_session(teams):
    sess=ranking.Seeding(teams)
    return sess

def fit_session(session,Games):
    games = session['games']
    teams = make_teams(session['teams'])
    sess = init_session(teams)
    sess.games = mcmc_games([Games[id] for id in games],
                                teams)
    sess.fit_model()
    return sess

def update_results(session,Games):
    
    sess = fit_session(session,Games)
    
    
    #should return some percent done thing. (contained in sess)
    err = 0
    if not err:
        pass
        #update a flag in 
    return sess.strengths()

def update_kl_info(session):

    sess = fit_session(sc)
    kl_vec = sess.kl_info_vec()
    return kl_vec

def get_best_staging(session,Games,kl_vec,r):
    teams = sc.make_teams(sc.get_team_list())
    n_teams = len(teams)

    sess = init_session(teams)

    sess.games = mcmc_games([games[id] for id in session['games']],
                                teams)
    game_list =  sess.stage_round(r,kl_vec)
    return game_list

