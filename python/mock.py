import ranking
import random
import statistics as stats
import math
from tournament import Team

def score_choices(max_score):
    choices = []
    for ii in range(0,max_score):
        for jj in range(0,max_score):
            choices = choices + [[ii,jj]]
    return choices

def discrete_lahiri(pr_f,choices):
    pr = 0
    u = 1
    while pr < u:
        x = random.choice(choices)
        pr = pr_f(x)
        u = random.uniform(0,1)
    return x

def generate_session(n_teams):
    teams = []
    strengths = [random.uniform(-2,2) for n in range(n_teams)]
    strengths = [s - stats.mean(strengths) for s in strengths]
    
    def m_team(id):
        t = Team()
        t.id = id
        t.session_id = id
        t.strength = strengths[id]
        return t
    teams = map(m_team, range(n_teams))    
    sess=ranking.Seeding(teams)
    return sess
        
def generate_round(sess,r):
    kl_vec = sess.kl_info_vec()
    games = sess.stage_round(r,sess.kl_info_dict(kl_vec))
    
    
    def prob_f(strengths,scores):
        return math.exp(sess.prob_func(strengths[1]-strengths[0],sess.scale,scores[1],scores[0]))
    
    def sample_scores(game):
        strengths = [t.strength for t in game.teams]
        pr_f = lambda x: prob_f(strengths,x)
        return discrete_lahiri(pr_f,score_choices(sess.max_score))
    
    for g in games:
        g.scores = sample_scores(g)
        
    sess.games = sess.games + games
    return sess

