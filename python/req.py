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
    sess = db['Sessions'][id]
    str_dict = bayes.update_results(Sessions[1],Games)
    for k,v in str_dict:
        sess['strengths'][k] = v

    return db

def update_score(db,game_id,score_dict):
    db['Games'][game_id]['scores']=score_dict
    db['Games'][game_id]['status']=1
    
    return db

def new_game(team_1,team_2,round):
    return {'team_1':team_1,'team_2':team_2,
            'round':round,'scores':{team_1:0,team_2:0},
            'status':0}

def get_suggested_games(db,session_id,round):
    kl = bayes.update_kl_info(Sessions[1],Games)
    games = bayes.get_best_staging(Sessions[1],Games,kl,2)
    db['Sessions'][session_id]['suggestedGames'] = games
    return db

def add_suggested_games(db,session_id):
    for g in db['Sessions'][session_id]['suggestedGames'].values():
        add_game(db,session_id,g)

    return db