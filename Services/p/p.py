from flask import Flask, request, send_file
import requests
from swiftclient.client import Connection, ClientException
from credentials import *

app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])

def getImage():
	try:
		user_id = request.args.get('user_id')
		#image = "images/"+str(user_id)+".jpg"
		image = str(user_id)+".jpg"
		#print("*******Image:", image)
		swiftimage = getImageSwift(image, "ContainerB")
		return send_file(swiftimage, mimetype='image/jpg')
    	except FileNotFoundError:
        	return "NoFile"

def getSwiftConn():
	return Connection(**get_session_credentials())

def getPicture(pictureToGet,containerName):
	conn = getSwiftConn()
	picture = conn.get_object(containerName, pictureToGet)
	return picture

if __name__ == '__main__':
	app.run(host = "ServerP", port=80)
