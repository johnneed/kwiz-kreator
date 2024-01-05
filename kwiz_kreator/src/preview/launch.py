import json
import os.path
import webbrowser
from threading import Timer

from flask import Flask, Response

app = Flask(__name__)
app.config.from_object(__name__)


def get_mime_type(path):
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
        ".ico": "image/x-icon",
        ".json": "application/json",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".svg": "image/svg+xml",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".ttf": "font/ttf",
        ".eot": "font/eot",
        ".otf": "font/otf",
        ".gif": "image/gif",
        ".txt": "text/plain",
    }
    ext = os.path.splitext(path)[1]
    return mimetypes.get(ext, "text/html")


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__)) + '/build/'


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/', methods=['GET'])
def get_main_file():  # pragma: no cover
    content = get_file('index.html')
    return Response(content, mimetype="text/html")


@app.route('/<path:path>', methods=['GET'])
def get_resources(path):
    print("GETTING RESOURCE: ", path, end="\n")
    complete_path = os.path.join(root_dir(), path)
    print("ABS PATH: ", complete_path, end="\n")
    mimetype = get_mime_type(complete_path)
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)


@app.route('/static/js/<path:path>', methods=['GET'])
def get_js(path):  # pragma: no cover
    print("GETTING JS: ", path, end="\n")
    complete_path = os.path.join(root_dir() + "static/js/", path)
    print("ABS PATH: ", complete_path, end="\n")
    mimetype = get_mime_type(complete_path)
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)


@app.route('/static/css/<path:path>', methods=['GET'])
def get_css(path):  # pragma: no cover
    print("GETTING CSS: ", path, end="\n")
    complete_path = os.path.join(root_dir() + "static/css/", path)
    print("ABS PATH: ", complete_path, end="\n")
    mimetype = get_mime_type(complete_path)
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)


def open_browser():
    webbrowser.open_new("http://localhost:3000")


def save_preview_quiz(trivia_data):  # pragma: no cover
    file_path = os.path.join(root_dir(), "trivia.json")
    try:
        with open(file_path, 'w') as outfile:
            json.dump(trivia_data, outfile)
            outfile.close()

    except Exception as e:
        print("Error: Unable to save to file " + file_path + " " + str(e))


def preview_quiz(trivia_json):
    save_preview_quiz(trivia_json)
    launch_preview_server()


def launch_server():
    app.run(port=3000)


def launch_preview_server():
    Timer(1, launch_server).start()
    Timer(2, open_browser).start()
