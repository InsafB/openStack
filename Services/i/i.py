from flask import Flask,render_template, request
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import json

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def identification():
	# Database config
	db = MySQLdb.connect(host='localhost', user="root", passwd="othmane", db="open_stack")
	cur = db.cursor()
	# Get master request with user_id
	user_id = request.args.get('user_id')
	cur.execute("SELECT first_name, last_name, email FROM users WHERE id = %s;", [user_id])
	if cur.rowcount==0:
		cur.close()
		db.close()
		error = {"error": "Invalid_ID"}
		return json.dumps(error)
	else:
		for (a, b, c) in cur:
			firstname = a
			lastname = b
			email = c
		cur.close()
		db.close()
		user={"firstname":firstname, "lastname":lastname, "email":email}
		return json.dumps(user)

if __name__ == '__main__':
	#app.run(host = socket.gethostbyname(socket.gethostname()), port=80)
	app.run(host='ServerI', port=80)
