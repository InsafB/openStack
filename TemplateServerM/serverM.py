from flask import Flask
from flask_mail import Mail, Message
from flask import render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'test.apps.email.2017@gmail.com'
app.config['MAIL_PASSWORD'] = 'test.apps'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

B_outofservice = "dontknow"
W_outofservice = "dontknow"

@app.after_request
def add_header(r):
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache" 
	r.headers["Expires"] = "0"
	r.headers['Cache-Control'] = 'public, max-age=0'
	return r

@app.route("/")
def hello():
	return "<h1>No ID provided</h1>"

@app.route("/play",methods=['POST', 'GET'])
def PlayButton():
	print("-----has entered B")
	user_id = request.args.get('user_id') 
	global B_outofservice
	global W_outofservice
	try:
		W_outofservice = "dontknow"
		responseB=CallB(user_id)
		B_outofservice="no"
		msg = Message('Notification: Promotional lottery-Open Stack',
			sender = 'test.apps.email.2017@gmail.com', recipients = ['ouiame.aitelkadi@gmail.com'])
		msg.body = "Hello, the user "+str(user_id)+" has just played. \nTeam."
		mail.send(msg)
		#print("**ResponseB:", type(responseB.content.decode("utf-8")), responseB.content )
		if str(responseB.content.decode("utf-8"))=="W_out":
			W_outofservice="yes"
		else:
			W_outofservice="no"
		#print("********Inside B - W_out", W_outofservice)
	except requests.ConnectionError:
		B_outofservice="yes"
		#print("*-*-*-*-*-* Inside B: Error!!", B_outofservice)
	return redirect("/"+str(user_id))

@app.route("/<id>")
def CallServices(id):
	global B_outofservice
	global W_outofservice
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

	# Detect if server P is down
	try:
		responseP=CallP(id)
		P_outofservice="no"
	except requests.ConnectionError:
		P_outofservice="yes"

	# Initialise flask variables	
	error = firstname = lastname = email = time = image_prize = ""
	
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
	else:
		hasplayed="dontknow"
	
	if P_outofservice=="no":
		if responseP.content=="NoFile":
			hasplayed="no"
		else:
			with open("static/image.jpg", "wb") as fb:
				fb.write(responseP.content)
			image_prize="image.jpg"

	#print("**********Before render: W_out", W_outofservice)
	W_state = W_outofservice
	B_state = B_outofservice
	W_outofservice="dontknow"
	B_outofservice="dontknow"
	return render_template('index.html', 
		I_outofservice=I_outofservice, error=error, id=id, firstname=firstname, lastname=lastname, email=email,
		S_outofservice=S_outofservice, hasplayed=hasplayed, time=time,
		B_outofservice=B_state, image_prize=image_prize,
		P_outofservice=P_outofservice, W_outofservice=W_state)

def CallI(idu):
	url = 'http://ServerI:80'
	param_user = {'user_id': idu}
	user = requests.get(url, params=param_user)
	response = json.loads(user.text)	
	return response

def CallS(idu):
	url = 'http://ServerS:80'
	param_user = {'user_id': idu}
	state = requests.get(url, params=param_user)
	response = json.loads(state.text)	
	return response

def CallB(idu):
	url = 'http://ServerB:80'
	param_user = {'user_id': idu}
	button = requests.get(url, params=param_user)	
	return button

def CallP(idu):
	url = 'http://ServerP:80'
	param_user = {'user_id': idu}
	image = requests.get(url, params=param_user)	
	return image

if __name__ == "__main__":
	app.run(host=ServerM, port=80)
