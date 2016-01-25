""" Worker for a session.

    Each running session gets a worker. Once initilized it's waiting for updates to run the bayesian stuff"""


""" Update a tournament score + KL graphA
    1) 

    1) read in data
        1a) somehow get address
        1b) read in games from redis (ENV variables)
        
    2) run MCMC
        2a) set computing flag
        2b) set up computation
        2c) run MCMC computation
        
    3) evaluate rankings
        3a) evaluate rankings
        3b) write to redis
        3c) flip rankings up-to-date flag (redis)
    
    4) build KL info graph
        4a) evaluate KL for each pair of teams
        4b) write to """


import redis
import os
import evaluate
import conn
from rq import Queue

#main loop


def main(session):
    s_ind = session['s_ind']
    session_key = "".join(["s:",str(s_ind)])

    redis_host = 'localhost'#os.environ['REDIS_HOST']
    redis_port = '6379'#os.environ['REDIS_PORT']
    wait_time = 1#os.environ['WAIT_TIME']
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
    q = Queue(connection=redis.Redis())

    sess = evaluate.init_session(sc.make_teams(dc.get_team_list()))
    
    
    #high = Queue('high', default_timeout=8)  # 8 secs
    #low = Queue('low', default_timeout=600)  # 10 mins
   # job = q.enqueue_call(func=mytask, args=(foo,), kwargs={'bar': qux}, timeout=600)  # 10 mins
    
    
    #q.enqueue(send_report, depends_on=report_job)

    
    def update_results():
        games = sc.get_games(r)
        teams = sc.make_teams(dc.get_team_list())
        new_sess = evaluate.init_session(teams)
        result = q.enqueue_call(func=evaluate.update_results,
                                args=games, timeout=wait_time)
        
        return result

    def get_best_stage(round_num,kl_graph,games):
        pass
    messages = {'update_results':update_results,
                'get_best_stage':get_best_stage}


    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe('session-channel')
    
    while True:
        # Deal with a message.
        message = p.get_message()
        if message:
            data = message['data'].split
            r_func = message[data[0]]
        # Check if something is updating. If it's updating post results.
        time.sleep(wait_time)  # be nice to the system :)



