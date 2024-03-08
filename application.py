from flask import Flask, request, redirect, url_for
import json
import os
import sys
import uuid
import http.client

from azure.core.exceptions import AzureError
#from azure.cosmos import CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from pymongo.mongo_client import MongoClient

app = Flask(__name__)

# connecting to cosmos db
client = MongoClient("mongodb://li-c-436p4-server:0Thk4cHi5Y0rLkelh4VB0Coxz2hpZY2fot03kUDh12rj6fW8oXMleZhwplJmQRJKQDzIb5F7LEndACDb8hGngw==@li-c-436p4-server.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@li-c-436p4-server@")
database = client["436p4DB"]
dbCollect = database["storedData"]

# connecting to azure blob
account_url = "https://cs41003200113807a1f.blob.core.windows.net"
default_credential = DefaultAzureCredential()

# Create the BlobServiceClient object
blobContainerName = "436p4"
blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=cs41003200113807a1f;AccountKey=2Nljt9xH0Ry2YrCbWppi5C/lhx7CWxu6NIzeyQ9mAuLHyzIPG7aiGGrwKmm8GOe5lx0FsMV5MANj+AStdXc2xw==;EndpointSuffix=core.windows.net")
container_client = blob_service_client.get_container_client("436p4")

@app.route("/", methods=["POST", "GET"])
def init_interface():
    if request.method == "POST":
        # when prompted to load data
        if request.form["button"] == "Load Data":
            # getting data
            get_blob = BlobClient("https://css490.blob.core.windows.net", "lab4", "input.txt")
            blob = get_blob.download_blob()
            blob_text = blob.readall()

            # making copy in azure blob storage
            container_client.upload_blob("input.txt", blob_text, "BlockBlob", overwrite=True)

            # parsing data
            text = str(blob_text)
            text = text[2:len(text) - 1]
            people = text.split("\\r\\n")

            # storing data
            #id = 0 # getting easy way to identify each person
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
                #id += 1

            # notify user
            return '''<h1>data loaded</h1?'''
        elif request.form["button"] == "Clear Data":
            # delete everything from azure blob and cosmos db
            if container_client.get_blob_client("input.txt").exists():
                container_client.delete_blob("input.txt")
                dbCollect.delete_many({})
                return '''<h1>Data cleared.</h1>'''
            else:
                return '''<h1>Currently no data to clear.</h1>'''
        elif request.form["button"] == "Query":
            input1 = request.form["fName"]
            input = request.form["lName"]
            # searching database or blob
            # displaying results in new page
            return f'''<h1>input: {input1} + {input}</h1>'''
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

@app.route("/input")
def input(input):
    return '''<h1>input: {input}</h1>'''
