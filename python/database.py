import csv
import os
import csv
def DB_init():
    DB = {}
    pwd = os.getcwd()
    team_file = "".join([pwd,'/teams.csv'])
    def teams_reader():
        def kv(row):
            return int(row[3]), {'session':row[0],'wc':bool(row[1]=='True'),
                            'name':row[2],'id':int(row[3])}

        team_dict = {}
        with open(team_file, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                k,v = kv(row)
                team_dict[k] = v
        return team_dict


    DB['Teams'] = teams_reader()

    for v in DB['Teams'].values():
            v['strength'] = 0


    def id_to_name(id):
        return DB['Teams'][id]['name']

    team_dict = DB['Teams']



    wc_teams = [k for k,v in team_dict.iteritems() if v['wc']]
    f_teams = [k for k,v in team_dict.iteritems() if (not v['wc'])]
    wc_teamsA = [k for k,v in team_dict.iteritems() if v['wc'] and (v['session']=='A')]
    wc_teamsB = [k for k,v in team_dict.iteritems() if v['wc'] and (v['session']=='B')]
    f_teamsA = [k for k,v in team_dict.iteritems() if (not v['wc']) and (v['session']=='A')]
    f_teamsB = [k for k,v in team_dict.iteritems() if (not v['wc']) and (v['session']=='B')]

    def initilize_sessions():
        wc_day_1am = {'id':1,'name':'Wildcard: Day 1 AM','type':'swiss','teams':wc_teamsA}
        wc_day_1pm = {'id':2,'name':'Wildcard: Day 1 PM','type':'swiss','teams':wc_teamsB}
        wc_day_2am = {'id':3,'name':'Wildcard: Day 2 AM','type':'swiss','teams':[]}
        wc_day_2pm = {'id':4,'name':'Wildcard: Day 2 PM','type':'swiss','teams':[]}
        f_day_1am = {'id':5, 'name':'Worlds: Day 1 AM','type':'swiss','teams':f_teamsA}
        f_day_1pm = {'id':6, 'name':'Worlds: Day 1 PM','type':'swiss','teams':f_teamsB}
        f_day_2am = {'id':7, 'name':'Worlds: Day 2 AM','type':'swiss','teams':[]}
        f_day_2pm = {'id':8, 'name':'Worlds: Day 2 PM','type':'swiss','teams':[]}
        f_day_3groups = {'id':9, 'name':'Worlds: Day 3 Group Stage','type':'group','teams':[]}
        f_day_3knockout = {'id':10, 'name':'Worlds: Day 3 Knockout Stage','type':'knockout','teams':[]} 
        
        sessions = {1:wc_day_1am, 2:wc_day_1pm,3:wc_day_2am,4:wc_day_2pm,
                    5:f_day_1am,6:f_day_1pm,7:f_day_2am,8:f_day_2pm,
                    9:f_day_3groups,10:f_day_3knockout}
        for v in sessions.values():
            v['games'] = []
            v['suggestedGames'] = []
            v['strengths'] = {}
            for id in v['teams']:
                v['strengths'][id] = 0

        return sessions


    DB['Sessions'] = initilize_sessions()

    def initilize_games():
        games = {}
        return games

    DB['Games'] = initilize_games()

    courts = {ind:{'id':ind,
                   'just_played':None,
                   'on_court':None,
                   'up_next':[],
                   'name':''.join(['Court ',str(ind)])} for ind in range(1,4)}
    DB['Courts'] = courts 
    return DB
