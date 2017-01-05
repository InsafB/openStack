from flask import Flask
from flask import render_template
import requests
import json

app = Flask(__name__)

@app.route("/")
def hello():
	return "<h1>No ID provided</h1>"

@app.route("/<id>")
def CallServices(id):
	# Detect if server I is down
	try:
		responseI=CallI(id)
		I_outofservice="no"
	except requests.ConnectionError:
		I_outofservice="yes"
	
	# Detect if server S is down
	try:
		responseS=CallS(id)
		S_outofservice="no"
	except requests.ConnectionError:
		S_outofservice="yes"
	
	# Initialise flask variables	
	error = firstname = lastname = email = hasplayed = time = ""
	
	if I_outofservice=="no":
		if 'error' in responseI:
			error = responseI['error']
		else:
			firstname = responseI['firstname']
			lastname = responseI['lastname']
			email = responseI['email']

	if S_outofservice=="no":
		hasplayed = responseS['hasplayed']
		time = responseS['time']
	
	return render_template('index.html', I_outofservice=I_outofservice, error=error, id=id, firstname=firstname, lastname=lastname, email=email, S_outofservice=S_outofservice, hasplayed=hasplayed, time=time)

def CallI(idu):
	url = 'http://ServerI:5050'
	param_user = {'user_id': idu}
	user = requests.get(url, params=param_user)
	response = json.loads(user.text)	
	return response

def CallS(idu):
	url = 'http://ServerS:5050'
	param_user = {'user_id': idu}
	state = requests.get(url, params=param_user)
	response = json.loads(state.text)	
	return response

if __name__ == "__main__":
	app.run(host=ServerM, port=5050)
