from flask import Flask,render_template, request
import MySQLdb
import json

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def identification():
	# Database config
	db = MySQLdb.connect(host="ServerI", user="root",passwd="othmane", db="USERS")
	cur = db.cursor()
	# Get master request with user_id
	user_id = request.args.get('user_id')
	cur.execute("SELECT first_name, last_name, email FROM users WHERE id = %s;", [user_id])
	if not cur.fetchone():
		error = {"error": "Invalid ID"}
		return json.dumps(user)
	else:
		for (a, b, c) in cur:
			firstname = a
			lastname = b
			email = c
		cur.close()
		db.close()
		user={"firstname":firstname,"lastname":lastname,"email":email}
		return json.dumps(user)

if __name__ == '__main__':
	app.run(host = "ServerI", port=5050)

	

