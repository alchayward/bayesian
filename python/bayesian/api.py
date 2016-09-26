from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions
import handlers as h
import tournament as tour
import rq
import os
from database import R
app = FlaskAPI(__name__)

# define api:
#    tournament
#       teams
#       session
#           add, remove, stage next games, get ranking
#           teams
#               add, get
#               team_id
#            games
#               add game
#               game
#                   score, teams
#

#   Teams
#        team
#           members
#           id
#           name
#   Games
#       game
#           teams
#           scores


def make_route(path):
    return "/".join(path)


def no_response():
    return None


def respond(call, methods):
    return methods.get(call, no_response)()


def route_struct(path, methods):
    return None


t_route = {'path': ['tournaments'], 'methods': {'GET': lambda : db['tournaments'],
                             'POST': lambda data: h.new_tournament(tour.new_tournament())}

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
