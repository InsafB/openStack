from flask import Flask
from flask import request
import socket
import requests
import base64
import os
import json
from swiftclient.client import Connection, ClientException
from credentials import *

app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def playLaunch():
    
    '''# POST with form-encoded data
    response = requests.post(url, data=payload)'''

    user_id = request.args.get('user_id')
    url = 'http://ServerW:5050/play/'+user_id
    #url = 'http://0.0.0.0:8090/play/1'
    
    # GET with params in URL
    response = requests.get(url)
    #Receive data and create img
    byte = json.loads(response.text)
    image = bytes(byte['img'], 'ascii')
    with open("imageToSave.png", "wb") as fh:
        fh.write(base64.decodestring(image))

    # Save image in swift
    puchImageSwift("imageToSave.png",user_id+".png","containerB")

    #delete tmp file
    os.remove("imageToSave.png")

    # Add user to status DB
    url = 'https://ServerS:5050/save/'
    payload = {'user_id': user_id}
    # GET with params in URL
    #response = requests.get(url, params=payload)

    return "True"
    
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
    app.run(host = '10.0.1.7', port=80)
    
