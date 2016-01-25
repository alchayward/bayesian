"""module docstring"""

# imports
import pickle
# constants
# exception classes
# interface functions
# classes
class Tournament:

    def __init__(self):
      self.sections = []
      self.name = ''
      self.id = 0
      self.href = ''
      teams = []
      
    def n_teams(self):
        return len(self.teams)

    def add_new_session(self,teams,class_name):
        for ind,t in enumerate(teams):
            t.session_id = ind
        
        S = class_name(teams)
        S.id = len(self.sections)
        self.sections.append(S)
 
    def save_tournament(self,filename):
        with open(filename,'w') as f:
            pickle.dump(self,f)
    
    def load_tournament(self,filename):
        with open(filename,'r') as f:
            self = pickle.load(filename)
        
        
    def print_t_team_list(self):
        for t in self.teams:
            print('{} -- {}:({}, {}, {})'.format(t.id,t.name,t.members[0].name,
                             t.members[1].name,t.members[2].name) )

       
class Team:

   default_name = 'No Name'

   def __init__(self):
      self.id = None
      self.name = Team.default_name
   
class Player():
    
    def __init__(self):
        self.name = ''
        self.city = ''
        pass

class Game:

   def __init__(self, teams = [], scores = [], round = 1, id = None):
     self.id = id
     self.teams = teams
     self.scores = scores
     self.round = round;
     if not self.scores:
        self.completed = False
     else:
        self.completed = True


class Round():
    
    def __init__(self, round_number = 1, games = []):
        self.games = games
        self.round_number = round_number
        

class Section():
    """Class which contaions information such as games, teams and 
    rounds, about a session.
    """

    def __init__(self,teams):
        """Type will be one of the tournament types:
        (session,braket)
        """
        #super(self.__class__,self).__init__()
        self.games = [] #Games should be a game object
        self.teams = teams
        self.id = 0


class Session():
   
    def __init__(self,teams):
        #super(self.__class__,self).__init__()
        #Section.__init__(self)

        self.games = [] #Games should be a game object
        self.teams = teams
        self.id = 0
        self.rounds = []

    def add_game(self, game = None):
        if game == None:
            self.print_team_list()
            print('team 1 ID')
            t1 = input()
            print('team 2 ID')
            t2 = input()
            print('team 1 score')
            s1 = input()
            print('team 2 score')
            s2 = input()
            print('which round?')
            round = input()
            if s1==s2:
                prompt = '{} tied with {}, at {} all. is this right?'.format(
                        self.teams[t1].name,self.teams[t2].name,s1)
            elif s1 > s2:   
                prompt = '{} bested {}, {}-{}. is this right?'.format(
                        self.teams[t1].name,self.teams[t2].name,s1,s2)
            else:   
                prompt = '{} bested {}, {}-{}. is this right?'.format(
                        self.teams[t2].name,self.teams[t1].name,s2,s1)
            print(prompt)
            print('enter 1 for yes')
            all_good = input()
            if all_good == 1:
                g = Game(
                    teams = [self.teams[t1],self.teams[t2]],
                    scores = [s1,s2])           
                g.round = round
                g.played = True
                self.games.append(g)
        else:
            prompt = '{} vs {}\n score for {}: '.format(
                    game.teams[0].name,game.teams[1].name,game.teams[0].name)
            print(prompt)
            s1 = input() 
            prompt = 'score for {}: '.format(
                    game.teams[1].name)
            print(prompt)
            s2 = input() 
            prompt = '{} vs {}, {}-{}. is this right?'.format(
                    game.teams[0].name,game.teams[1].name,s2,s1)
            print(prompt)
            all_good = input()
            if all_good:
                game.scores = [s1,s2]
                game.played = True
                #self.games.append(game)
    def print_game_list(self,games = None):
        if games == None:
            games = self.games
        for g in games:
            if g.played:               
                print('{} vs {}: {} -- {}'.format(
                    g.teams[0].name,g.teams[1].name,
                    g.scores[0],g.scores[1]))
            else:
                print('{} vs {}: unplayed'.format(
                    g.teams[0].name,g.teams[1].name) )
    
    def print_team_list(self,members = False):
        for t in self.teams:
            if members:
                print('{} -- {}:({}, {}, {})'.format(
                    t.session_id,t.name,t.members[0].name,
                    t.members[1].name,t.members[2].name) )
            else:
                 print('{} -- {}'.format( t.session_id,t.name) )
    

class Swiss(Section):

   def __init__(self):
      pass

class Elim(Section):

   def __init__(self):
      pass

class DoubleElim(Section):

   def __init__(self):
      pass

# internal functions & classes

