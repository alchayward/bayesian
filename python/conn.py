from tournament import Team, Game

def read_list(list_string):
    return map(int,list_string)

data_structure = {'s_ids':0,
                  't_ids':0,
                  'm_ids':[0,1,2],
                  's':{'t_ids':[0,1],
                       'game_ids':[0,1],
                       'game':{ 'id':0,
                                'team_1':0,
                                'team_2':1,
                                'score_1':-1,
                                'score_2':-1,
                                'round':0,
                                's_updated':0,
                                'kl_updated':0,
                                'status':0}},
                  'team':{'name':'none','members':[0,1,2]},
                  'member':{'name':'me',
                            'city':'timaru'}}

game_properties = data_structure['s']['game'].keys()
default_game = data_structure['s']['game']

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

class SessionConnection:

    def __init__(self,session_key,r_conn):
        self.session_key=session_key
        self.r_conn=r_conn 
    
    def team_list_key(self):
        return "".join([self.session_key,":t_ids:"])

    def write_map(self,key,dmap):
        for id, value in dmap.iteritems():
            self.r_conn.hset(key,id,str(value))

    def read_map(self,key):
        d = self.r_conn.hgetall(key)
        for key,val in d.iteritems():
            d[key] = num(val)
        return d
        
    def new_game_id_key(self):
        return "".join([self.session_key,":new_game_id"])

    def game_key(self,game_id):
        return "".join([self.session_key,":game:",str(game_id)])
        
    def games_list_key(self):
        return "".join([self.session_key,":game_ids"])
    
    def strength_key(self,team_id):
        return "".join([self.session_key,":strengths:",str(team_id)])
    
    def kl_key(self,ind):
        return "".join([self.session_key,":kl:",str(ind)])
    
    def get_team_list(self):
        return read_list(self.r_conn.lrange(self.team_list_key(),0,-1))

    def get_game_list(self):
        return read_list(self.r_conn.lrange(self.games_list_key(),0,-1))

    def get_game_property(self,id,prop):
        return num(self.r_conn.hget(self.game_key(id),prop))
    
    def get_game(self,game_id):
        return self.read_map(self.game_key(game_id))
    
    def get_games(self):
        game_list = self.get_game_list()
        return dict(zip(game_list,
                        [self.get_game(id) for id in game_list]))
    
    def set_strengths(self,team_strengths):
        for team_id in team_strengths:
            self.r_conn.set(self.strength_key(team_id),
                            team_strengths[team_id])
    
    def set_kl_edge(self,ind,val):
        key = self.kl_key(ind)
        self.write_map(key,val)

    def set_kl_vec(self,kl_vec):
        for ind,val in enumerate(kl_vec):
            self.set_kl_edge(ind,val)

    def get_kl_edge(self,kl_vec,ind):
        key = self.kl_key(ind)
        return self.read_map(key)

    def get_kl_vec(self,kl_inds):
        kl_vec =  [self.read_map(self.kl_key(ind)) for ind in kl_inds]
        return filter(lambda x: x, kl_vec) 

    def set_game_property(self,game_id,prop,val):
        self.r_conn.hset(self.game_key(game_id),prop,val)

    def new_game_id(self):
        key = self.new_game_id_key()
        id = int(self.r_conn.get(key))
        self.r_conn.incr(key)
        return id
        
    def set_game(self,game):
        id = game['id']
        game_key = self.game_key(id)
        for key,val in game.iteritems():
            self.r_conn.hset(game_key,key,str(val))
    
    def make_teams(self,team_ids):

        def new_team(id,ind):
            t = Team()
            t.id = id
            t.session_id = ind
            return t
        
        return [new_team(ind,id) for ind,id in enumerate(team_ids)]
        
    def mcmc_games(self,games,teams):
        teams_dict = dict(zip([t.session_id for t in teams],teams))
        
        def new_game(id):
            g = Game()
            game = games[id]
            g.id = id
            g.teams = [teams_dict[game['team_1']],teams_dict[game['team_2']]]
            if not game['status'] == 1:
                g.scores = None
            else:
                g.scores = [game['score_1'],game['score_2']]
            g.round = game['round']
            return g
        
        return [new_game(id) for id in games]

    def stage_list_key(self):
        return "".join([self.session_key,":stage_list"])

    def clear_stage_list(self):
        key =  self.stage_list_key()
        self.r_conn.delete(key)

    def set_stage_game(self,game):
        id = self.new_game_id()
        g = default_game
        g['id'] = id
        teams = [t.id for t in game.teams]
        g['team_1'] = teams[0]
        g['team_2'] = teams[1]
        g['round'] = game.round
        self.set_game(g)
        self.r_conn.rpush(self.stage_list_key(),id)

