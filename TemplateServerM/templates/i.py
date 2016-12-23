from flask import Flask, session, redirect, url_for, escape, request, render_template
from hashlib import md5
import MySQLdb

app = Flask(__name__)

# Database config
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="test")
cur = db.cursor()


'''
If you have the Flask.secret_key set you can use sessions in Flask applications. 
A session basically makes it possible to remember information from one request to another.
The way Flask does this is by using a signed cookie.
So the user can look at the session contents, but not modify it unless they know the secret key,
usually something complex and unguessable
'''

@app.route('/')
def index():
    # Verify if a session is already open
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        # Save the user's name, and render the index template ( with the name of the user -- done with flask code in index.html )
        return render_template('index.html', session_user_name=username_session)
    return redirect(url_for('login'))


@app.route('/login/<int:id>', methods=['GET', 'POST'])
def login():
    error = None
    user_id = None
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_form  = request.form['username']
        password_form  = request.form['password']
        cur.execute("SELECT COUNT(1) FROM users WHERE name = %s;", [username_form])
        # if no name is fetched
        if not cur.fetchone()[0]:
            error = "Invalid login"
        else:
            cur.execute("SELECT password,user_id FROM users WHERE name = %s;", [username_form])
            # Password is hashed -- compare the hashes
            if md5(password_form).hexdigest() == cur[1][0]:
                session['username'] = request.form['username']
                user_id = cur[1][1]
                return redirect(url_for('index'))
            else:
                error = "Invalid password"
            
    return render_template('index.html', error=error, id=user_id)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.secret_key = 'just a simple secret key'

if __name__ == '__main__':
    app.run(debug=True)
