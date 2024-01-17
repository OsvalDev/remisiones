from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_mysqldb import MySQL
import os
from flask_sqlalchemy import SQLAlchemy 

from controllers.loginController import login as funLogin
from controllers.userController import *
from controllers.costumersController import *
from controllers.remissionController import *
from controllers.followController import *
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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://userp:oY9u463?e@p3nwplsk12sql-v17.shr.prod.phx3.secureserver.net:1433/dbclientesm?driver=ODBC+Driver+17+for+SQL+Server'
db_sql_server = SQLAlchemy(app)

#get routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    user = verifyUser()

    if user[0]:
        remissionList = getRemissions(mysql)
        return render_template('dashboard.html', user = user[1], canDo = user[2], remissionList = remissionList)
    else:
        return redirect(url_for('login'))
    
@app.route('/users')
def users():
    user = verifyUser()

    if user[0]:
        data = getUsers(mysql, user[0])
        areas = getAreas(mysql, user[0])
        admin = verifyAdmin(mysql, user[0])

        return render_template('users.html', user = user[1], userList = data, areas = areas, admin = admin , canDo = user[2])
    else:
        return redirect(url_for('login'))

@app.route('/costumers')
def costumers():
    user = verifyUser()

    if user[0]:
        admin = verifyAdmin(mysql, user[0])
        costumerList = getCostumers(mysql)        
        return render_template('costumers.html', user = user[1], canDo = user[2],  admin = admin, costumerList = costumerList)
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/remission/<idRemission>/<idCompra>')
def remissionList(idRemission, idCompra):
    user = verifyUser()
    result = getRemissionDetail(mysql, idRemission, idCompra)
    if user[0]:
        admin = verifyAdmin(mysql, user[0])
        
        return render_template('remissionDetail.html', user = user[1], admin = admin , canDo = user[2], data = result)
    else:
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
    
@app.route('/turnOffUser', methods= ['POST'])
def turnOffUser():    
    user = verifyUser()

    if user[0]:
        id = request.form['idUser']
        editStatusUser(mysql, id, 0)
        return redirect(url_for('users'))
    else:
        return redirect(url_for('login'))
@app.route('/turnOnUser', methods= ['POST'])
def turnOnUser():    
    user = verifyUser()

    if user[0]:
        id = request.form['idUser']
        editStatusUser(mysql, id, 1)
        return redirect(url_for('users'))
    else:
        return redirect(url_for('login'))

@app.route('/sync', methods= ['POST'])
def sync():    
    result = syncClientDb(db_sql_server, mysql)
    return jsonify( result )

@app.route('/nameCostumer', methods= ['POST'])
def nameCostumer():    
    data = request.get_json()
    result = getCostumerName(mysql, data)
    return jsonify( result )

@app.route('/newRemission', methods= ['POST'])
def newRemission():
        
    user = verifyUser()

    if user[0]:
        data = {
            'numCompra' : request.form['numCompra'],
            'numRemission' : request.form['numRemission'],
            'numCliente' : request.form['numCliente'],
            'piezas' : request.form['piezas'],
            'remisionado' : request.form['remisionado'],
            'facturado' : request.form['facturado']
        }
        
        addRemission(mysql, data)
        
        return redirect(url_for('dashboard'))

    else:
        return redirect(url_for('login'))

@app.route('/confirmDeliver/<idRemission>/<idCompra>', methods = ['POST'] )
def confirmDeliver(idRemission, idCompra):

    user = verifyUser()

    if user[0]:
        date = request.form['dateConfirm']

        registerDateConfirmation(mysql, date, idRemission, idCompra)
        urlDetail = '/registro/remission/' + str(idRemission) + '/' + str(idCompra)
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))
    
    
if __name__ == '__main__':
    app.run()