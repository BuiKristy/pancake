from flask import Flask, render_template, send_file, request, redirect, url_for
from mutagen import File
from io import BytesIO
from database import DB_connection
import os 
import json

app = Flask(__name__)

@app.route('/list')
def list_music():
    path = r"music"
    result = []

    for song in os.listdir(path):
        result.append(song)

    return render_template("list.html", list=result)

@app.route('/picture/<song_name>')
def get_picture(song_name):
    path = r"music"
    file = File(os.path.join(path, song_name))
    try:
        if file.pictures:
            return send_picture(file.pictures[0].data)
    except AttributeError:
        if "APIC:" in file.tags:
            return send_picture(file.tags["APIC:"].data)
    
    return send_file(r"static\no_image.jpg")

def send_picture(artwork):
    image = BytesIO()
    image.write(artwork)
    image.seek(0)
    return send_file(image, mimetype='image/jpeg')

@app.route('/model')
def get_json_model():
    model = dict()
    model['playlists'] = []

    for playlist_id, playlist_name in DB_connection.get_playlists().items():
        playlist_map = dict()
        playlist_map['id'] = playlist_id
        playlist_map['name'] = playlist_name
        playlist_map['songs'] = DB_connection.get_songs_from_playlist(playlist_id)
        model['playlists'].append(playlist_map)
    
    print(model)
    return json.dumps(model)
    
@app.route('/playlists', methods=['POST', 'GET'])
def handle_playlists():
    if request.method == 'POST':
        playlist_id = DB_connection.create_playlist(request.form['playlist_name'])
        return "", 201, {'location': '/playlists/' + str(playlist_id)}
    elif request.method == 'GET':
        return json.dumps(DB_connection.get_playlists())

@app.route('/playlists/<int:playlist_id>', methods=['DELETE', 'PATCH', 'POST', 'GET'])
def modify_playlist(playlist_id):
    if playlist_id not in DB_connection.get_playlists():
        abort(404)
    if request.method == 'DELETE':
        DB_connection.delete_playlist(playlist_id)
        return ""
    elif request.method == 'PATCH':
        DB_connection.update_playlist_name(playlist_id, request.form['playlist_name'])
        return "", 204
    elif request.method == 'POST':
        DB_connection.add_song_to_playlist(playlist_id, request.form['song'])
        playlist = DB_connection.get_songs_from_playlist(playlist_id)
        return "", 201, {'location': '/playlists/' + str(playlist_id) + '/' + str(len(playlist) - 1)}
    elif request.method == 'GET':
        return json.dumps(DB_connection.get_songs_from_playlist(playlist_id))

@app.route('/playlists/<int:playlist_id>/<int:song_index>', methods=['DELETE', 'PATCH', 'GET'])
def modify_song(playlist_id, song_index):
    if playlist_id not in DB_connection.get_playlists():
        abort(404)
    length = len(DB_connection.get_songs_from_playlist(playlist_id))
    if 0 <= song_index < length:
        if request.method == 'DELETE':
            DB_connection.delete_song_from_playlist(playlist_id, song_index)
            return ""
        elif request.method == 'GET':
            return DB_connection.get_songs_from_playlist(playlist_id)[song_index]
        elif request.method == 'PATCH':
            new_index = request.form['new_index']
            try:
                if 0 <= new_index < length:
                    DB_connection.reorder_songs_in_playlist(playlist_id, song_index, \
                        request.form['new_index'])
                    return "", 204
                else:
                    abort(404)
            except:
                abort(404)
    else:
        abort(404)

@app.route('/')
def show_app():
    path = r"music"
    return render_template("app.html", playlists=DB_connection.get_playlists(), songs=os.listdir(path))