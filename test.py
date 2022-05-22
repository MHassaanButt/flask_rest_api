import sqlite3
# from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Flask, jsonify, request, session
# pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
from flask_mysqldb import MySQL, MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS  # pip install -U flask-cors
from datetime import timedelta
# from flask.ext.cors import CORS, cross_origin

from datetime import timedelta
conn = sqlite3.connect('database.db')
print("Opened database successfully")

# conn.execute(
#     'CREATE TABLE user (id INT, username TEXT, password TEXT)')
print("Table created successfully")

conn.close()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'cairocoders-ednalan'

# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
# CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testingdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def home():
    passhash = generate_password_hash('cairocoders')
    print(passhash)
    if 'username' in session:
        username = session['username']
        return jsonify({'message': 'You are already logged in', 'username': username})
    else:
        resp = jsonify({'message': 'Unauthorized'})
        resp.status_code = 401
        return resp


@app.route('/login', methods=['POST'])
def login():
    _json = request.json
    _username = _json['username']
    _password = _json['password']
    print(_password)
    # validate the received values
    if _username and _password:
        # check user exists
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        sql = "SELECT * FROM user WHERE username=%s"
        sql_where = (_username,)

        cursor.execute(sql, sql_where)
        row = cursor.fetchone()
        username = row['username']
        password = row['password']
        if row:
            if check_password_hash(password, _password):
                session['username'] = username
                cursor.close()
                return jsonify({'message': 'You are logged in successfully'})
            else:
                resp = jsonify({'message': 'Bad Request - invalid password'})
                resp.status_code = 400
                return resp
    else:
        resp = jsonify({'message': 'Bad Request - invalid credendtials'})
        resp.status_code = 400
        return resp


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message': 'You successfully logged out'})


if __name__ == "__main__":
    app.run()
