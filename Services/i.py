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
    cur.execute("SELECT firstname, lastname, email FROM users WHERE id = %s;", [user_id])
    if not cur.fetchone():
        error = "Invalid id"
        return error
    else:
        for (firstname, lastname, email) in cur:
            return firstname, lastname, email
cur.close()
db.close()

if __name__ == '__main__':
    app.run(host = socket.gethostbyname(socket.gethostname()))
