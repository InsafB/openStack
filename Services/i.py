from flask import Flask,render_template, request
import MySQLdb

app = Flask(__name__)

# Database config
db = MySQLdb.connect(host="ServerI", user="root", passwd="othmane", db="USERS")
cur = db.cursor()

@app.route('/',methods=['GET', 'POST'])
def identification():
    # Get master request with user_id
    user_id = request.args.get('user_id')
    error = None
    cur.execute("SELECT first_name, last_name, email FROM users WHERE id = %d;", [user_id])
    if not cur.fetchone()[0]:
        error = "Invalid id"
        return error
    else:
        firstname = cur[1][0]
        lastname = cur[1][1]
        email = cur[1][2]
        return user_id, firstname, lastname, email
db.close()

if __name__ == '__main__':
    app.run(host = socket.gethostbyname(socket.gethostname()))
