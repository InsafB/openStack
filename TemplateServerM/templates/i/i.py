from flask import Flask,render_template
import MySQLdb

app = Flask(__name__)

# Database config
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="test")
cur = db.cursor()

@app.route('/<int:id>')
def identification():
    error = None
    user_id = id
    cur.execute("SELECT COUNT(1) FROM users WHERE id = %d;", [user_id])
    # if id not found
    if not cur.fetchone()[0]:
        error = "Invalid id"
        return render_template('index.html', error=error)
    else:
        cur.execute("SELECT first_name, last_name, email FROM users WHERE id = %d;", [user_id])            
        return render_template('index.html', id=user_id, firstname = cur[1][0], lastname = cur[1][1], email = cur[1][2] )

if __name__ == '__main__':
    app.run(debug=True)
