from flask import Flask
from flask import request
import socket


app = Flask(__name__)

@app.route("/")
def scanUser():
    username = request.args.get('username')
    password = request.args.get('password')
    if lookupUser(username,password):
        return True
    else:
        return False

def lookupUser(username,password):

    with open('users.csv', 'r') as File:
        for line in File:
            fields=line.split(":")
            if username in fields and password in fields:
                return True
        return False

if __name__ == "__main__":

    app.run(host = socket.gethostbyname(socket.gethostname()))