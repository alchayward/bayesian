import ranking
import time
import conn
import redis
import os
from rq import Queue

def init_session(teams):
    sess=ranking.Seeding(teams)
    return sess

def fit_session(sc):
    games = sc.get_games()
    teams = sc.make_teams(sc.get_team_list())
    sess = init_session(teams)
    sess.games = sc.mcmc_games(games,teams)
    sess.fit_model()
    return sess

def update_results(session_key,r):
    
    sc = conn.SessionConnection(session_key,r)
    sess = fit_session(sc)
    strengths = dict(zip([id for id in teams],sess.strengths()))
    
    # Communication to the outside world
    sc.set_strengths(strengths)
    for id in games:
        sc.set_game_property(id,'s_updated',1)
    
    #should return some percent done thing. (contained in sess)
    err = 0
    if not err:
        pass
        #update a flag in 
    return err

def update_kl_info(session_key,r):

    sc = conn.SessionConnection(session_key,r)
    sess = fit_session(sc)

    # Might as well update results here too.  (premature optimization...)
    sc.set_strengths(strengths)
    for id in games:
        sc.set_game_property(id,'s_updated',1)

    kl_vec = sess.kl_info_vec()
    sc.set_kl_vec(kl_vec,sess.marginal_ind)
    for id in games:
        sc.set_game_property(id,'s_updated',1)
    err = 0
    return err

def get_best_staging(session_key,r,round_num):
    sc = conn.SessionConnection(session_key,r)
    kl_vec = sc.get_kl_vec()
    
    game_list =  sess.stage_round(round_num)
    err = 0
    return game_list,err

