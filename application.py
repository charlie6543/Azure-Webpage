from flask import Flask, request, redirect, url_for
import json
import os
import sys
import uuid

from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from pymongo.mongo_client import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://li-c-436p4-server:0Thk4cHi5Y0rLkelh4VB0Coxz2hpZY2fot03kUDh12rj6fW8oXMleZhwplJmQRJKQDzIb5F7LEndACDb8hGngw==@li-c-436p4-server.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@li-c-436p4-server@")
database = client["436p4DB"]
dbCollect = database["storedData"]

# Create the BlobServiceClient object
blobContainerName = "436p4"
blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=cs41003200113807a1f;AccountKey=2Nljt9xH0Ry2YrCbWppi5C/lhx7CWxu6NIzeyQ9mAuLHyzIPG7aiGGrwKmm8GOe5lx0FsMV5MANj+AStdXc2xw==;EndpointSuffix=core.windows.net")
container_client = blob_service_client.get_container_client("436p4")

@app.route("/", methods=["POST", "GET"])
def init_interface():
    if request.method == "POST":
        # when prompted to load data
        if request.form["button"] == "Load Data":
            return redirect(url_for("load"))
        elif request.form["button"] == "Clear Data":
            return redirect(url_for("clear"))
        elif request.form["button"] == "Query":
            fInput = request.form["fName"]
            lInput = request.form["lName"]

            if(fInput == "" and lInput == ""):
                return redirect(url_for("queryAll"))
            if(fInput == ""):
                return redirect(url_for("queryL", lName = lInput))
            elif(lInput == ""):
                return redirect(url_for("queryF", fName = fInput))
            # searching database
            return redirect(url_for("query", fName = fInput, lName = lInput))
    else:
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

@app.route("/load")
def load():
    # connect to db
    client = MongoClient("mongodb://li-c-436p4-server:0Thk4cHi5Y0rLkelh4VB0Coxz2hpZY2fot03kUDh12rj6fW8oXMleZhwplJmQRJKQDzIb5F7LEndACDb8hGngw==@li-c-436p4-server.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@li-c-436p4-server@")
    database = client["436p4DB"]
    dbCollect = database["storedData"]
    
    # Create the BlobServiceClient object
    blobContainerName = "436p4"
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=cs41003200113807a1f;AccountKey=2Nljt9xH0Ry2YrCbWppi5C/lhx7CWxu6NIzeyQ9mAuLHyzIPG7aiGGrwKmm8GOe5lx0FsMV5MANj+AStdXc2xw==;EndpointSuffix=core.windows.net")
    container_client = blob_service_client.get_container_client("436p4")

    # getting data
    get_blob = BlobClient("https://css490.blob.core.windows.net", "lab4", "input.txt")
    blob = get_blob.download_blob()
    blob_text = blob.readall()

    # parsing data
    text = str(blob_text)
    text = text[2:len(text) - 1]
    contentSettings = ContentSettings(content_type='text/plain')
    container_client.upload_blob("input.txt", text, "BlockBlob", overwrite=True, content_settings=contentSettings)
    text = text.replace("\\t", " ")
    people = text.split("\\r\\n")

    # storing data
    for person in people:
        attributes = person.split() # getting list of attributes
        # creating item with id, firstName, and lastName
        new_item = {
            "firstName": attributes[1],
            "lastName": attributes[0],
        }

        # going through all attribtues and adding them to the item
        for attribute in attributes[2:]:
            keyValue = attribute.split("=")
            new_item[keyValue[0]] = keyValue[1]

        # adding to db
        dbCollect.update_one({"firstName": attributes[1]}, {"$set": new_item}, upsert=True)

    client.close()
    blob_service_client.close()

    # notify user
    return '''<form action="#" method="post">
    <h1>Data has been loaded! Queries are now updated.<h1>
    <p>Go back to previous page to query.</p>'''

@app.route("/clear")
def clear():
    # connect to db
    client = MongoClient("mongodb://li-c-436p4-server:0Thk4cHi5Y0rLkelh4VB0Coxz2hpZY2fot03kUDh12rj6fW8oXMleZhwplJmQRJKQDzIb5F7LEndACDb8hGngw==@li-c-436p4-server.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@li-c-436p4-server@")
    database = client["436p4DB"]
    dbCollect = database["storedData"]
    
    # Create the BlobServiceClient object
    blobContainerName = "436p4"
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=cs41003200113807a1f;AccountKey=2Nljt9xH0Ry2YrCbWppi5C/lhx7CWxu6NIzeyQ9mAuLHyzIPG7aiGGrwKmm8GOe5lx0FsMV5MANj+AStdXc2xw==;EndpointSuffix=core.windows.net")
    container_client = blob_service_client.get_container_client("436p4")

    # delete everything from azure blob and cosmos db
    if container_client.get_blob_client("input.txt").exists():
        container_client.delete_blob("input.txt")
        dbCollect.delete_many({})
        client.close()
        blob_service_client.close()
        return '''<h1>Data cleared.</h1>'''
    else:
        client.close()
        blob_service_client.close()
        return '''<h1>Currently no data to clear.</h1>'''

@app.route("/queryAll")
def queryAll():
    # connect to db
    client = MongoClient("mongodb://li-c-436p4-server:0Thk4cHi5Y0rLkelh4VB0Coxz2hpZY2fot03kUDh12rj6fW8oXMleZhwplJmQRJKQDzIb5F7LEndACDb8hGngw==@li-c-436p4-server.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@li-c-436p4-server@")
    database = client["436p4DB"]
    dbCollect = database["storedData"]
    results = dbCollect.find({})
    resultString = "<h1>Results:</h1>"
    for result in results:
        resultString += "<p>" + str(result) + "</p>"

    client.close()
    return resultString


@app.route("/query/<string:fName>_<string:lName>")
def query(fName, lName):
    # connect to db
    client = MongoClient("mongodb://li-c-436p4-server:0Thk4cHi5Y0rLkelh4VB0Coxz2hpZY2fot03kUDh12rj6fW8oXMleZhwplJmQRJKQDzIb5F7LEndACDb8hGngw==@li-c-436p4-server.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@li-c-436p4-server@")
    database = client["436p4DB"]
    dbCollect = database["storedData"]

    # searching database
    results = None
    if(fName == ""):
        results = dbCollect.find({"lastName": lName})
    elif(lName == ""):
        results = dbCollect.find({"firstName": fName})
    else:
        results = dbCollect.find({"firstName": fName, "lastName": lName})
    resultString = "<h1>Results matching " + lName + ", " + fName + ":</h1>"
    for result in results:
        resultString += "<p>" + str(result) + "</p>"

    client.close()
    
    # displaying results in new page
    return resultString

@app.route("/queryF/<string:fName>_")
def queryF(fName):
    # connect to db
    client = MongoClient("mongodb://li-c-436p4-server:0Thk4cHi5Y0rLkelh4VB0Coxz2hpZY2fot03kUDh12rj6fW8oXMleZhwplJmQRJKQDzIb5F7LEndACDb8hGngw==@li-c-436p4-server.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@li-c-436p4-server@")
    database = client["436p4DB"]
    dbCollect = database["storedData"]

    # searching database
    results = None
    results = dbCollect.find({"firstName": fName})
    resultString = "<h1>Results matching " + fName + ":</h1>"
    for result in results:
        resultString += "<p>" + str(result) + "</p>"

    client.close()
    
    # displaying results in new page
    return resultString

@app.route("/queryL/_<string:lName>")
def queryL(lName):
    # connect to db
    client = MongoClient("mongodb://li-c-436p4-server:0Thk4cHi5Y0rLkelh4VB0Coxz2hpZY2fot03kUDh12rj6fW8oXMleZhwplJmQRJKQDzIb5F7LEndACDb8hGngw==@li-c-436p4-server.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@li-c-436p4-server@")
    database = client["436p4DB"]
    dbCollect = database["storedData"]

    # searching database
    results = dbCollect.find({"lastName": lName})
    resultString = "<h1>Results matching " + lName + ":</h1>"
    for result in results:
        print(result)
        resultString += "<p>" + str(result) + "</p>"

    client.close()
    
    # displaying results in new page
    return resultString
