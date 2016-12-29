from flask import Flask,render_template
import MySQLdb

app = Flask(__name__)

# Database config
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="test")
cur = db.cursor()

@app.route('/<int:id>')
def status():
    state = None
    user_id = id
    cur.execute("SELECT COUNT(1) FROM played WHERE id = %d;", [user_id])
    # if id not found
    if not cur.fetchone()[0]:
        return render_template('index.html', state=False)
    else:
        cur.execute("SELECT time FROM played WHERE id = %d;", [user_id])            
        return render_template('index.html', state=True, time=cur[1][0])

if __name__ == '__main__':
    app.run(debug=True)
