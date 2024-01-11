from flask import Flask, render_template, redirect, url_for, request, make_response, jsonify, session
from flask_mysqldb import MySQL
import os
from datetime import datetime

from controllers.loginController import login as funLogin
from controllers.userController import *
from utils.userSession import verifyUser

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = '198.12.216.200'
app.config['MYSQL_USER'] = 'i9694026_wp1'
app.config['MYSQL_PASSWORD'] = 'C4rn1v4L2311*'
app.config['MYSQL_DB'] = 'remisiones'

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'carnival*c1rn2v3l-1a23i4a5/c4rn1v4l.'

mysql = MySQL(app)

#get routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    user = verifyUser()

    if user[0]:
        return render_template('dashboard.html', user = user[1], canDo = user[2])
    else:
        return redirect(url_for('login'))
    
@app.route('/users')
def users():
    user = verifyUser()

    if user[0]:
        data = getUsers(mysql, user[0])
        areas = getAreas(mysql, user[0])

        return render_template('users.html', user = user[1], userList = data, areas = areas, canDo = user[2])
    else:
        return redirect(url_for('login'))

@app.route('/costumers')
def costumers():
    user = verifyUser()

    if user[0]:
        return render_template('costumers.html', user = user[1], canDo = user[2])
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

#post routes
@app.route('/login', methods= ['POST'])
def postLogin():    
    data = request.get_json()    
    result = funLogin(mysql, data)
    
    if result[1]['result'] == 'failed':
        return jsonify( result[1] )
    else:
        session['user_id'] = data['id']
        session['user_name'] = result[0]
        session['privilegiesList'] = result[2]
        return jsonify( result[1] )

@app.route('/newUser', methods= ['POST'])
def newUser():    

    user = verifyUser()

    if user[0]:
    
        idWorker = request.form['idWorker']
        name = request.form['name']
        password = request.form['password']
        area = request.form['area']

        data = [idWorker, name, password, area]
        addUser(mysql, data)

        return  redirect(url_for('users'))
    else:
        return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run()