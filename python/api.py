from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions
import rq
import os
app = FlaskAPI(__name__)



class DB(object): # make sure you inherit from object

    def __init__():

    @property
    def data(self):
        return 4
    def set

p = Test()
p.x # returns 4

def init_DB():
DB = {}
pwd = os.getcwd()
team_file = "".join([pwd,'/teams.csv'])

    with open(


DB = init_DB()

redis_host = 'localhost'#os.environ['REDIS_HOST']
redis_port = '6379'#os.environ['REDIS_PORT']
wait_time = 1#os.environ['WAIT_TIME']
r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
q = Queue(connection=redis.Redis())

def do_job(f,argss):

    job = q.enqueue_call(func=f, args=argss, timeout=wait_time)
    @propery
    DB = lambda : job.result or DB




def team_ranking_text(session,team):
pass

def note_repr(key):
    return {
        'url': request.host_url.rstrip('/') + url_for('teams', key=key),
        'text': notes[key]
    }

@app.route("/", methods=['GET', 'POST'])
def notes_list():
    """
    List or create notes.
    """
    if request.method == 'POST':
        note = str(request.data.get('text', ''))
        idx = max(notes.keys()) + 1
        notes[idx] = note
        return note_repr(idx), status.HTTP_201_CREATED

    # request.method == 'GET'
    return [note_repr(idx) for idx in sorted(notes.keys())]


@app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def notes_detail(key):
    """
    Retrieve, update or delete note instances.
    """

    # request.method == 'GET'
    if key not in notes:
        raise exceptions.NotFound()
    return session_repr(key)


@app.route("/<int:key>/update_scores", methods=['POST', 'GET'])
def notes_detail(key):
    """
    Retrieve, update or delete note instances.
    """
    if request.method == 'POST':
        update_scores(key)
        return score_update_status(key)

    # request.method == 'GET'
    if key not in DB['Sessions'].keys():
        raise exceptions.NotFound()
    return score_update_status(key)


@app.route("/<int:key>/stage_round/", methods=['POST', 'GET'])
def notes_detail(key):
    """
    Retrieve, update or delete note instances.
    """
    if request.method == 'POST':
        stage_round(key,request.data.post('round', ''))
        return staged_games_text(key)

    # request.method == 'GET'

    if key not in DB['Sessions'].keys():
        raise exceptions.NotFound()
    return staged_games_text(key)

@app.route("/<int:key>/stage_round/<int:r>", methods=[ 'GET'])
def notes_detail(key,r):
    """
    Retrieve, update or delete note instances.
    """
    # request.method == 'GET'

    if request.method == 'POST':
        stage_round(key,request.data.post('round', ''))
        return stage_update_status_req(key)

    if key not in DB['Sessions'].keys():
        raise exceptions.NotFound()
        if stage_update_status():
            return stage
    return stage_update_status_req(key)
if __name__ == "__main__":
    app.run(debug=False)

