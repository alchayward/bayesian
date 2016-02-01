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
    
    return {id:new_team(ind,id) for ind,id in enumerate(team_ids)}


def mcmc_games(games,teams):
    
    def new_game(game):
        g = Game()
        g.id = game['id']
        t1 = game['team_1']
        t2 = game['team_2']
        g.teams = [teams[t1],teams[t2]]
        if not game['status'] == 1:
            g.scores = None
        else:
            g.scores = [game['scores'][t1],
                        game['scores'][t2]]
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

def update_kl_info(session,Games):

    sess = fit_session(session,Games)
    kl_vec = sess.kl_info_vec()
    return kl_vec

def mc_game_to_dict(mc_game):
    return {'status':0,
            'id':mc_game.id,
            'team_1':mc_game.teams[0].id,
            'team_2':mc_game.teams[1].id,
            'scoores':{mc_game.teams[0].id:0,mc_game.teams[1].id:0},
            'score_1':None,
            'score_2':None,
            'round':mc_game.round}

def get_best_staging(session,Games,kl_vec,r):
    teams = make_teams(session['teams'])
    sess = init_session(teams)
    games = session['games']
    sess.games = mcmc_games([Games[id] for id in games],
                                teams)

    game_list =  sess.stage_round(r,kl_vec)
    for ind,g in enumerate(game_list):
        g.id = ind

    new_games = map(mc_game_to_dict,game_list)
    return dict(zip([g['id'] for g in new_games],new_games)) 
