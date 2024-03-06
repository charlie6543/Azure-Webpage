from flask import Flask, request, redirect, url_for
#import json
#import os
#import sys

#from azure.core.exceptions import AzureError
#from azure.cosmos import CosmosClient, PartitionKey

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def init_interface():
    if request.method == "POST":
        if request.form["button"] == "Load Data":
            return f'''<h1>data loaded {client}</h1?'''
        elif request.form["button"] == "Clear Data":
            return '''<h1>data cleared</h1>'''
        elif request.form["button"] == "Query":
            input1 = request.form["fName"]
            input = request.form["lName"]
            return f'''<h1>input: {input1} + {input}</h1>'''
    else:
        # when 'load' is hit, add data to database:
        # from this url:
        # https://css490.blob.core.windows.net/lab4/input.txt
        # copy data into oject storage in cloud
        # parse and load into database

        # when 'clear' is hit, remove data from everywhere

        # when query:
        # if nothing in database, return error
        # return matches from database
        return '''<form action="#" method="post">
        <h1>this is a website<h1>
        <input type="submit" name="button" value="Load Data"><br>
        <input type="submit" name="button" value="Clear Data"><br>
        <label for="fName">First Name</label>
        <input type="text" id'="fName" name="fName"/>
        <label for="lName">Last Name</label>
        <input type="text" id'="lName" name="lName"/>
        <input type="submit" name="button" value="Query"/>'''

@app.route("/input")
def input(input):
    return '''<h1>input: {input}</h1>'''
