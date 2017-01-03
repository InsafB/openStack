from flask import Flask,render_template,request
import socket
import MySQLdb
import requests
import time
import datetime

app = Flask(__name__)

# Database config
db = MySQLdb.connect(host="ServerS", user="root", passwd="othmane", db="STATUS")
cur = db.cursor()

@app.route("/",methods=['GET', 'POST'])
def scanUser():
    user_id = request.args.get('user_id')
    return lookupUser(user_id)

def lookupUser(user_id):
    cur.execute("SELECT user_id, time FROM played WHERE id = %d;", [user_id])
    if not cur.fetchone()[0]:
        return False
    else:
        time = cur[1][1]
        return True, time

@app.route("/save",methods=['GET', 'POST'])
def lookupUser():
    user_id = request.args.get('user_id')
    ts = time.time()
    time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("""INSERT INTO played VALUES (%s, %s);""", (user_id,time))
    db.commit()

db.close()

if __name__ == "__main__":
    app.run(host = socket.gethostbyname(socket.gethostname()))
