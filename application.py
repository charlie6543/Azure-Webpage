from flask import Flask

app = Flask(__name__)

@app.route("/")
def hexiyello_world():
    return "<p>Hello World!</p>"