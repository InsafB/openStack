from flask import Flask,render_template
import MySQLdb

app = Flask(__name__)

# Database config
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="test")
cur = db.cursor()

from flask import Flask
from flask import request
import socket


app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def scanUser():
    user_id = request.args.get('user_id')
    if lookupUser(user_id):
        return True
    else:
        return False

def lookupUser(user_id):
    with open('status.csv', 'r') as File:
        for line in File:
            if user_id == line:
                return True
        return False

@app.route("/save",methods=['GET', 'POST'])
def lookupUser():
    user_id = request.args.get('user_id')
    with open('status.csv', 'a') as File:
        File.write(user_id+"\n")
    return True


        

if __name__ == "__main__":

    app.run(host = socket.gethostbyname(socket.gethostname()))
