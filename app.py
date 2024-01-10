from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_mysqldb import MySQL
import hashlib
import os
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = '198.12.216.200'
app.config['MYSQL_USER'] = 'i9694026_wp1'
app.config['MYSQL_PASSWORD'] = 'C4rn1v4L2311*'
app.config['MYSQL_DB'] = 'cardscarnival'

app.config['UPLOAD_FOLDER'] = 'static/uploads'

mysql = MySQL(app)

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()