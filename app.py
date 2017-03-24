from flask import Flask, render_template, send_file
from mutagen import File
from io import BytesIO
import os 

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