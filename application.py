from flask import Flask

app = Flask(__name__)

@app.route("/")
def init_interface():
    return '''<h1>this is a website<h1>
    <button type="button">Load Data</button>
    <button type="button">Clear Data</button>
    <label for="fName">First Name</label>
    <input type="text" id'="fName" name="fName"/>
    <label for="lName">Last Name</label>
    <input type="text" id'="lName" name="lName"/>
    <button type="button">Query</button>'''
