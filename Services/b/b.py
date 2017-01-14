from flask import Flask
from flask import request
import socket
import requests
import base64
import os
import json
import binascii
from swiftclient.client import Connection, ClientException
from credentials import *

app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def playLaunch():
    user_id = request.args.get('user_id')
    try:
        url = 'http://ServerW:80/play/'+user_id
        # GET with params in URL
        response = requests.get(url)
        #Receive data from W and create img
        byte = json.loads(response.text)
        image = bytes(byte['img'], 'ascii')
        ###print("***Service B: image content before insert", image)
        image_name = "images/"+str(user_id)+".jpg"
        with open(image_name, "wb") as fh:
            fh.write(base64.decodestring(image))
        # Save image in swift
        puchImageSwift(image_name,user_id+".jpg","containerB")
        #delete tmp file
        os.remove(image_name)
        print("*********Service B: Image added**********")
    except:
        return "W_out"

    # Add user to status DB
    try:
        #print("********Service B: Call Service S: Save play")
        url = 'http://ServerS:80/save'
        payload = {'user_id': user_id}
        response = requests.get(url, params=payload)
        return "UserAdded"
    except requests.ConnectionError:
        return "S_out"    

@app.route("/test",methods=['GET', 'POST'])
def gettest():
    print(" request catched ")
    return " request catched "

def getSwiftConn():
    return Connection(**get_session_credentials())

def puchImageSwift(pictureToPut,pictureNewName,containerName):
    conn = getSwiftConn()
    with open(pictureToPut, 'rb') as f:
        file_data = f.read()
    conn.put_object(containerName, pictureNewName, file_data)
    print("Put Picture: Execution completed")   

if __name__ == "__main__":

    #app.run(host = socket.gethostbyname(socket.gethostname()), port=80)
    app.run(host = 'ServerB', port=80)
    
