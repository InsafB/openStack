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
		swiftimage = getPicture(image, "ContainerPrices")
		with open('static/image.jpg', 'wb') as my_picture:
			my_picture.write(swiftimage[1])
		return send_file("static/image.jpg", mimetype='image/jpg')
    	except:
        	return "NoFile"

def getSwiftConn():
	return Connection(**get_session_credentials())

def getPicture(pictureToGet,containerName):
	conn = getSwiftConn()
	picture = conn.get_object(containerName, pictureToGet)
	return picture

if __name__ == '__main__':
	app.run(host = "ServerP", port=80)
