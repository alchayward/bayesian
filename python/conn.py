from tournament import Team, Game

def read_list(list_string):
    return map(int,list_string)

data_structure = {'s_ids':list,
                  't_ids':list,
                  'm_ids':list,
                  's':{'t_ids':list,
                       'game_ids':list,
                       'game':{ 'team_1':int,
                                'team_2':int,
                                'score_1':int,
                                'score_2':int,
                                'round':int,
                                's_updated':int,
                                'kl_updated':int,
                                'status':int}},
                  'team':{'name':str,'members':list},
                  'member':{'name':str,
                            'city':str}}

game_properties = data_structure['s']['game'].keys()

class SessionConnection:

    def __init__(self,session_key,r_conn):
        self.session_key=session_key
        self.r_conn=r_conn 
    
    def team_list_key(self):
        return "".join([self.session_key,":t_ids:"])

    def game_key(self,game_id):
        return "".join([self.session_key,":game:",str(game_id)])
        
    def games_list_key(self):
        return "".join([self.session_key,":game_ids"])
    
    def strength_key(self,team_id):
        return "".join([self.session_key,":strengths:",str(team_id)])
    
    def kl_key(self,team1_id,team2_id):
        return "".join([self.session_key,":kl:t1:",str(team1_id),
                                           ':t2:',str(team2_id)])
    
    def property_key(self,game_id,prop):
        return "".join([self.game_key(game_id),':',prop])

    def get_team_list(self):
        return read_list(self.r_conn.lrange(self.team_list_key(),0,-1))

    def get_game_list(self):
        return read_list(self.r_conn.lrange(self.games_list_key(),0,-1))

    def get_game_property(self,id,prop):
        return int(self.r_conn.get(self.property_key(id,prop)))
    
    def get_game(self,game_id):
        game = {'id':game_id}
        for prop in game_properties:
            game[prop]=self.get_game_property(game_id,prop)
        return game
    
    def get_games(self):
        game_list = self.get_game_list()
        return dict(zip(game_list,
                        [self.get_game(id) for id in game_list]))
    
    def set_strengths(self,team_strengths):
        for team_id in team_strengths:
            self.r_conn.set(self.strength_key(team_id),team_strengths[team_id])
      
    def set_kl(self,kl_graph):
        for edge in kl_graph:
            self.r_conn.set(self.kl_key(edge['t1'],edge['t2']),edge['weight'])
        
    def set_game_property(self,game_id,prop,val):
        self.r_conn.set(self.property_key(game_id,prop),val)

    def set_game(self,game):
        id = game['id']
        for prop in game:
            self.set_game_property(id,prop,game[prop])
    
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
