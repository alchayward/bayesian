import ranking
import time
import conn
import redis
import os
from rq import Queue

def init_session(teams):
    sess=ranking.Seeding(teams)
    return sess

def update_results(session_key,r):
    
    sc = conn.SessionConnection(session_key,r)
    games = sc.get_games()
    teams = sc.make_teams(sc.get_team_list())
    sess = init_session(teams)
    sess.games = sc.mcmc_games(games,teams)
    sess.fit_model()
    strengths = dict(zip([id for id in teams],sess.strengths()))
    sc.set_strengths(strengths)
    for id in games:
        sc.set_game_property(id,'s_updated',1)
    
    sess.update_KL_graph()
    

    #should return some percent done thing. (contained in sess)
    err = 0
    if not err:
        pass
        #update a flag in 
    return sess.mcmc

def update_kl_info(sess):
    sess.update_KL_graph()
    err = 0
    return sess,err

def get_best_staging(sess,round_num):
    game_list =  sess.stage_round(round_num)
    err = 0
    return game_list,err

def test_func():
    time.sleep(3)
    print('done')
    return 1
