from flask import Flask,render_template,request
import socket
import MySQLdb
import time
import datetime
import json

app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def lookupUser():
    db = MySQLdb.connect(host=ServerS, user="root", passwd="othmane", db="open_stack")
    cur = db.cursor()
    user_id = request.args.get('user_id')    
    cur.execute("SELECT timeplay FROM plays WHERE id = %s;", [user_id])
    if cur.rowcount==0:
        cur.close()
        db.close()
        state = {"hasplayed": "no","time":""}
        return json.dumps(state)
    else:
        for a in cur:
            time_play = a
        cur.close()
        db.close()
        timeplay = time_play[0].strftime('%m-%d-%Y %H:%M:%S')
        state = {"hasplayed": "yes", "time": timeplay}
        return json.dumps(state)

@app.route("/save",methods=['GET', 'POST'])
def saveUser():
    db = MySQLdb.connect(host=ServerS, user="root", passwd="othmane", db="open_stack")
    cur = db.cursor()
    user_id = request.args.get('user_id')
    ts = time.time()
    time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("""INSERT INTO plays VALUES (%s, %s);""", (user_id,time))
    db.commit()
    cur.close()
    db.close()
    return "Done"

if __name__ == "__main__":
    #app.run(host = socket.gethostbyname(socket.gethostname()), port=80)
    app.run(host = ServerS, port=80)
