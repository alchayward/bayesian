import bayes

def add_game(db,session_id,game):
    #check id
    
    g_ids = [g['id'] for g in db['Games'].values()]
    if game['id'] in g_ids:
        game['id'] = max(g_ids) + 1

    db['Sessions'][session_id]['games'].append(game['id'])
    db['Games'][game['id']] = game
    return db

def update_strengths(db,session_id):
    sess = db['Sessions'][session_id]
    str_dict = bayes.update_results(db['Sessions'][1],db['Games'])
    for k,v in str_dict.iteritems():
        sess['strengths'][k] = v

    return db

def update_score(db,game_id,s1,s2):
    g = db['Games'][game_id]
    t1 = g['team_1']
    t2 = g['team_2']
    score_dict = {t1:s2,t2:s1}
    db['Games'][game_id]['scores']=score_dict
    db['Games'][game_id]['status']=1
    
    return db

def new_game(team_1,team_2,round):
    return {'team_1':team_1,'team_2':team_2,
            'round':round,'scores':{team_1:0,team_2:0},
            'status':0,'id':0}

def get_suggested_games(db,session_id,round):
    kl = bayes.update_kl_info(db['Sessions'][1],db['Games'])
    games = bayes.get_best_staging(db['Sessions'][1],db['Games'],kl,round)
    db['Sessions'][session_id]['suggestedGames'] = games
    return db

def add_suggested_games(db,session_id):
    for g in db['Sessions'][session_id]['suggestedGames'].values():
        add_game(db,session_id,g)

    return db

def remove_game(db,session_id,game_id):
    games = db['Sessions'][session_id]['games']
    games = filter(lambda x:not x == game_id,games)
    db['Sessions'][session_id]['games'] = games
    return db
