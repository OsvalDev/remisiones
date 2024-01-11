from flask import Flask, render_template, redirect, url_for, request, make_response, jsonify, session
from flask_mysqldb import MySQL
import os
from datetime import datetime

from controllers.loginController import login as funLogin

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
    return render_template('dashboard.html')

#post routes
@app.route('/login', methods= ['POST'])
def postLogin():    
    data = request.get_json()    
    result = funLogin(mysql, data)
    
    if result['result'] == 'failed':
        return jsonify( result )
    else:
        session['user_id'] = data['id']
        return jsonify( result )

if __name__ == '__main__':    
    app.run()