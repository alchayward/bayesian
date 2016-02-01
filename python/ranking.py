# Current problems/restrictions:
# Can't play the same team more than once.

import multiprocessing
import tournament 
from tournament import Session,Game
import networkx as nx
import numpy as np
import pymc
from scipy import cosh, rand, log
from scipy.special import gammaincc, gammaln
from numpy import dot,exp,array
#import matplotlib.pyplot as plt



def parfun(f,q_in,q_out):
    while True:
        i,x = q_in.get()
        if i is None:
            break
        q_out.put((i,f(x)))

def parmap(f, X, nprocs = multiprocessing.cpu_count()):
    q_in   = multiprocessing.Queue(1)
    q_out  = multiprocessing.Queue()

    proc = [multiprocessing.Process(target=parfun,args=(f,q_in,q_out)) for _ in range(nprocs)]
    for p in proc:
        p.daemon = True
        p.start()

    sent = [q_in.put((i,x)) for i,x in enumerate(X)]
    [q_in.put((None,None)) for _ in range(nprocs)]
    res = [q_out.get() for _ in range(len(sent))]

    [p.join() for p in proc]

    return [x for i,x in sorted(res)]

def log_2_pois_like(d,a,s1,s2): #taken out the max_score  limit for now
    dp = 1.0*np.arctan(d)
    return ( log(a)*(s1+s2)+dp*(s2-s1) -2*a*cosh(dp) -
             gammaln(s1+1) - gammaln(s2+1) )

def log_diff_exp_likr(d,a,s1,s2):
    return exp( (-(d + (s1-s2))**2)/a )


def log_d_pois_like_trunc_5(d,s1,s2,a):
    """double poisson w max 5 goals"""
    #dp = np.sign(d)*np.power(np.abs(d),p)
    dp = 1.5*np.arctan(d)    #print(dp)
    return ( log(a)*(s1+s2)+dp*(s1-s2) - 2*a*cosh(dp)
         -gammaln(s1+1) - gammaln(s2+1) 
        -log(gammaincc(6,a*exp(-dp))*gammaincc(6,a*exp(dp)) ) ) 
 

class double_model():
    
    def kl_func(self):
        scores = range(self.max_score+1)
        f = self.prob_func
        a = self.mcmc.scale.trace[:]
        trace = self.mcmc.marginal_delta.trace[:,:]
        def kl(ind):
            def expect(fn):
                return np.mean(fn(trace[:,ind]))
            
            Epr = np.array([[expect( lambda x: exp(f(x,a,s1,s2)))
                 for s1 in scores] for s2 in scores])
            Elogpr = np.array([[expect( lambda x: f(x,a,s1,s2) )
                 for s1 in scores] for s2 in scores])
            Eprlogpr = np.array( [[expect(lambda x: exp(f(x,a,s1,s2))*f(x,a,s1,s2)) 
                 for s1 in scores ] for s2 in scores])
        
            return np.sum(Eprlogpr)-np.sum(Epr*Elogpr)
        return kl  

    def strengths(self):
        strengths = self.mcmc.theta.stats()['mean']
        sd = {}
        for t in self.teams.values():
            ind = self.team_dict.get(t.id)
            if not ind is None:
                sd[t.id] = strengths[ind]
            else:
                sd[t.id] = 0

        return sd
        
    def get_data(self,games):
        n_games = len(games)
        data_games = []
        for g in games:
            if g.scores:
                data_games.append(g)
        
        teams = list(set([g.teams[0].id for g in games] +
                         [g.teams[1].id for g in games]))
        n_teams = len(teams)

        team_dict = dict(zip(teams,range(n_teams)))

        team_idx = np.zeros([len(data_games),n_teams])
        scores = []
        for ind,game in enumerate(data_games):
            score = [min(s,self.max_score) for s in game.scores]
            scores.append(game.scores)   
            team_idx[ind,team_dict[game.teams[0].id]] = 1
            team_idx[ind,team_dict[game.teams[1].id]] = -1
        
        self.team_dict = team_dict

        m_mat = np.zeros([n_teams*(n_teams-1)/2,n_teams]) 
        m_ind = []
        count = 0
        for ii in range(n_teams):
            for jj in range(ii+1,n_teams):
                m_mat[count,ii] = 1.0
                m_mat[count,jj] = -1.0
                m_ind.append([teams[ii],teams[jj]])
                count=count+1
        self.marginal_ind = m_ind
        return np.array(scores),np.array(team_idx),m_mat,n_teams

    def make_model(self):
        
        scores,team_idx,m_mat,n_teams = self.get_data(self.games)

        n_games = len(scores)
        prob_func = self.prob_func
        scale = self.scale
        #Just set as a constant now, too lazy
        scale = pymc.TruncatedNormal(
           'scale',mu = self.scale,
           tau = np.power(1/5.0,2),
           value=self.scale
           ,a = 0,b = 10)
        
        #expo = pymc.Uniform( 'expo',0.45,1,value=0.5)
        expo = 0.5

        #need to put in initial seeding stuff
        theta_i = pymc.Normal('theta_i',
                              mu = 0,
                              tau = np.power(1/3.0,2),
                              value=rand(n_teams)*0.00001)

        @pymc.deterministic()
        def theta(beta=theta_i):
            return beta - np.mean(beta)

        @pymc.stochastic(observed=True)
        def games_played(value=scores ,sp=scale,alpha = theta):
            return sum(prob_func(dot(team_idx, alpha), sp,
                 value[:,0], value[:,1]))
            
        @pymc.deterministic()
        def marginal_delta(beta = theta):
            return np.dot(m_mat,beta)
        
        return pymc.Model(locals())
    
    def fit_model(self):
        m = self.make_model()
        for key in m.__dict__.keys():
            if not isinstance(key, basestring):
                del m.__dict__[key]
        self.mcmc = pymc.MCMC(m)
        self.mcmc.use_step_method(pymc.AdaptiveMetropolis, self.mcmc.theta_i)
        print('running MCMC')
        self.mcmc.sample(self.mc_points,self.mc_burn ,self.mc_steps ,
             progress_bar=True)
    
    def __init__(self):
        # Model Parameters
        #self.n_teams = n_teams
        n_teams = self.n_teams
        #self.inital_theta = rand(self.n_teams)*0.0*3.0-1.5
        self.inital_theta = rand(self.n_teams)*0.00001
        self.prob_func = log_2_pois_like

        self.max_score = 10
        self.scale = 2.0
        
        # MC parameters
        self.mc_points = 100
        self.mc_burn = 10
        self.mc_steps = 1
        self.mcmc=None
        
        #KL Info init

    def kl_info_vec(self):
        m = self.marginal_ind
        n = len(m)
        t_ids = [t.id for t in self.teams.values()]
        def f_fun(ii):
            return (m[ii][0] in t_ids) and (m[ii][1] in t_ids)
        inds = filter(f_fun,range(n))
        if self.mcmc == None:
            f = lambda x:0
        else:
            f = self.kl_func()
        weights =  parmap(f,inds)
        print(inds)
        return [{'t1':m[ii][0],'t2':m[ii][1],'weight':weights[ii]} for ii in inds]

    def kl_info_dict(self,kl_vec):
        g={}
        n= self.n_teams
        def inner_dict(ii):
           ts = filter(lambda x:not x == ii,range(n))
           return dict(zip(ts, 
            [None for jj in ts]))

        d = dict(zip(range(n),
                [inner_dict(ii) for ii in range(n)]))
        for ind,e in enumerate(self.marginal_ind):
            d[e[0]][e[1]] = kl_vec[ind]
            d[e[1]][e[0]] = kl_vec[ind]
        return d
    
    def stage_teams(self,edge_list,kl_info):
        """Pass a list of team-team indices that need to be staged"""
        f_list = [(e[0],e[1],{'weight':0}) for e in edge_list]

        for d in kl_info: 
            try:
                ii=f_list.index([d['t1'],d['t2']])
            except ValueError:
                pass
            else:
                f_list[ii] = (d['t1'],d['t2'],{'weight':d['weight']})
                
            try:
                ii=f_list.index([d['t2'],d['t1']])
            except ValueError:
                pass
            else:
                f_list[ii] = (d['t2'],d['t1'],{'weight':d['weight']})

        F= nx.Graph()
        F.add_edges_from(f_list)
        return nx.max_weight_matching(F)

class Seeding(Session,double_model):
    """Adaptive style seeding section"""

    def __init__(self,teams): 
        self.n_teams = len(teams)
        
        #super(self.__class__, self).__init__()
        double_model.__init__(self)
        Session.__init__(self,teams)
        #self.current_round = tournament.Round(1)

    def get_teams_to_seed(self,round):
        rgames = filter(lambda g:g.round == round,self.games)
        rteams = [[t.id for t in g.teams] for g in rgames]
        nt_list = []
        for sublist in rteams:
            for val in sublist:
                nt_list.append(val)

        ids = [t.id for t in self.teams.values() if t.id not in nt_list]
        neg_list = []   
        for g in self.games:
            if g.round <= round:
                neg_list.append([t.id for t in g.teams])
        edge_list = []
        print(neg_list)
        for ii in ids:
            for jj in filter(lambda x: not x==ii,ids):
                if not  any([ [ii,jj] in neg_list, [jj,ii] in neg_list]):
                    edge_list.append([ii,jj])
        return edge_list

    def stage_round(self,round,kl_info):
        e_list = self.get_teams_to_seed(round)
        stage = self.stage_teams(e_list,kl_info)
        games = [ [k, stage[k] ] for k in stage.keys()]
        game_list = []
        gg_list = []
        for g in games:
            if not [g[1],g[0]] in gg_list:
                gg_list.append(g)
                game = tournament.Game(
                    teams = [self.teams[g[0]],self.teams[g[1]]])
                game.staged = False
                game.completed = False
                game.round = round
                game_list.append(game)
        return game_list


