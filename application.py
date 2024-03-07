from flask import Flask, request, redirect, url_for
import json
import os
import sys
import uuid
import http.client

from azure.core.exceptions import AzureError
from azure.cosmos import CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

DB_NAME = "li-c-436p4-server"
COLLECTION_NAME = "Collection1"

app = Flask(__name__)

# connecting to cosmos db
client = CosmosClient.from_connection_string("AccountEndpoint=https://li-c-436p4-server.documents.azure.com:443/;AccountKey=0Thk4cHi5Y0rLkelh4VB0Coxz2hpZY2fot03kUDh12rj6fW8oXMleZhwplJmQRJKQDzIb5F7LEndACDb8hGngw==")
databases = client.list_databases(10) # testing print databases
for database in databases:
    print(database)

# connecting to azure blob
account_url = "https://cs41003200113807a1f.blob.core.windows.net"
#credentials = ClientSecretCredential(tenant_id=)
default_credential = DefaultAzureCredential()

# Create the BlobServiceClient object
blobContainerName = "436p4"
blob_service_client = BlobServiceClient(account_url, credential=default_credential)
container_client = blob_service_client.get_container_client("436p4")

@app.route("/", methods=["POST", "GET"])
def init_interface():
    if request.method == "POST":
        if request.form["button"] == "Load Data":
            # getting data
            get_blob = BlobClient("https://css490.blob.core.windows.net", "lab4", "input.txt")
            blob = get_blob.download_blob()
            blob_text = blob.readall()
            container_client.upload_blob("input.txt", blob_text, "BlockBlob")

            text = str(blob_text)

            # parsing data
            text = text[2:len(text) - 1]
            people = text.split("\\r\\n")
            '''for ppl in people:
                print(ppl)
                print()'''

            # storing data
            for person in people:
                attributes = person.split()
                # lastName, firstName, attributes list
                # attributes do not need to be separated, just need to be printed
                # load to <key, value> format
                # then, from there, store the rest of the attributes
                #for attribute in attributes:
                    # parse vartype and then value
                    # store



            # notify user
            return '''<h1>data loaded</h1?'''
        elif request.form["button"] == "Clear Data":
            # delete everything from azure blob and cosmos db
            return '''<h1>data cleared</h1>'''
        elif request.form["button"] == "Query":
            input1 = request.form["fName"]
            input = request.form["lName"]
            # searching database or blob
            # displaying results in new page
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
