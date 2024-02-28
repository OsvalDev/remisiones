from flask import Flask, render_template, redirect, url_for, request, jsonify, session, Response
from flask_mysqldb import MySQL

from controllers.loginController import login as funLogin, loginCostumer
from controllers.userController import *
from controllers.costumersController import *
from controllers.costumerController import *
from controllers.remissionController import *
from controllers.followController import *
from controllers.appController import *
from controllers.chartController import *
from controllers.filterController import *
from utils.userSession import verifyUser, verifyCostumer
from utils.makePdf import getPdf as makePdf
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

@app.route('/amorcito')
def amorcito():
    return render_template('amor.html')

@app.route('/dashboard')
def dashboard():
    user = verifyUser()

    if user[0]:
        remissionList = getRemissions(mysql)
        costumerList = getActiveCostumerList(mysql)['data']
        estatusList = getEstatusList(mysql)['data']        
        return render_template('dashboard.html', user = user[1], canDo = user[2], remissionList = remissionList, costumers = costumerList, estatusList = estatusList)
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

@app.route('/autorizations')
def autorizations():
    user = verifyUser()

    if user[0]:
        data = getRemissionsByType(mysql, 1)
        costumerList = getActiveCostumerList(mysql)['data']
        estatusList = getEstatusList(mysql)['data']
        admin = verifyAdmin(mysql, user[0])

        return render_template('autorizations.html', user = user[1], admin = admin , canDo = user[2], data = data, costumers = costumerList, estatusList = estatusList)
    else:
        return redirect(url_for('login'))
@app.route('/supply')
def supply():
    user = verifyUser()

    if user[0]:
        data = getRemissionsToSupply(mysql)
        costumerList = getActiveCostumerList(mysql)['data']
        estatusList = getEstatusList(mysql)['data']
        admin = verifyAdmin(mysql, user[0])        
        return render_template('supply.html', user = user[1], admin = admin , canDo = user[2], data = data[0], existDate = data[1], costumers = costumerList, estatusList = estatusList)
    else:
        return redirect(url_for('login'))
@app.route('/logistics')
def logistics():
    user = verifyUser()

    if user[0]:
        data = getRemissionsToLogistic(mysql)
        costumerList = getActiveCostumerList(mysql)['data']
        estatusList = getEstatusList(mysql)['data']
        admin = verifyAdmin(mysql, user[0])
        return render_template('logistics.html', user = user[1], admin = admin , canDo = user[2],  data = data[0], existDate = data[1], costumers = costumerList, estatusList = estatusList)
    else:
        return redirect(url_for('login'))
@app.route('/delivery')
def delivery():
    user = verifyUser()

    if user[0]:
        data = getRemissionsByType(mysql, 3, 4, True)
        costumerList = getActiveCostumerList(mysql)['data']
        estatusList = getEstatusList(mysql)['data']
        admin = verifyAdmin(mysql, user[0])
        return render_template('delivery.html', user = user[1], admin = admin , canDo = user[2], data = data, costumers = costumerList, estatusList = estatusList)
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
        choferes = getChoferes(mysql)
        return render_template('remissionDetail.html', user = user[1], admin = admin , canDo = user[2], data = result, choferes = choferes)
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
    result = syncClientDb(mysql)
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

        data = request.get_json()
        
        result = addRemission(mysql, data)
        
        return jsonify(result)

    else:
        return jsonify({'result':'failed'})

@app.route('/editRemission', methods= ['POST'])
def editRemission():
        
    user = verifyUser()

    if user[0]:        

        data = {
            'numRemision' : request.form['numRemision'],
            'numCompra' : request.form['numCompra'],
            'piezas' : request.form['piezas'],
            'remisionado' : request.form['remisionado'],
            'facturado' : request.form['facturado'],
            'saldoAFavor' : request.form['bonificado'],
            'saldoInicial' : request.form['saldoInicial'],
            'numFactura' : request.form['numFactura']
        }
        
        changueRemission(mysql, data)
        
        urlDetail = '/registro/remission/' + str(data['numRemision']) + '/' + str(data['numCompra'])
        return redirect(urlDetail)

    else:
        return redirect(url_for('login'))

@app.route('/confirmDeliver/<idRemission>/<idCompra>', methods = ['POST'] )
def confirmDeliver(idRemission, idCompra):

    user = verifyUser()

    if user[0]:
        date = request.form['dateConfirm']

        registerDateConfirmation(mysql, date, idRemission, idCompra)
        if request.form['origin'] == 'many':
            urlDetail = '/registro/delivery'
        else:
            urlDetail = '/registro/remission/' + str(idRemission) + '/' + str(idCompra)
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))

@app.route('/dateCommit/<idRemission>/<idCompra>', methods = ['POST'] )
def dateCommit(idRemission, idCompra):

    user = verifyUser()

    if user[0]:
        data = {
            'accion' : request.form['action'],
            'fechaCompromiso' : request.form['dateConfirm'],
            'numRemision' : idRemission,
            'numCompra' : idCompra,
            'usuario' : user[0],
            'estatus' : 2 if request.form['action'] == 'Surtimiento' else 3
        }        

        registerDateCommit(mysql, data)
        if request.form['origin'] == 'many':
            if request.form['action'] == 'Logistica':
                urlDetail = '/registro/logistics'
            else:
                urlDetail = '/registro/supply'
        else:
            urlDetail = '/registro/remission/' + str(idRemission) + '/' + str(idCompra)
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))
    
@app.route('/parcelDelivery/<idRemission>/<idCompra>', methods = ['POST'] )
def parcelDelivery(idRemission, idCompra):

    user = verifyUser()

    if user[0]:
        data = {
            'user' : user[0],
            'parcelName' : request.form['parcelName'],
            'date' : request.form['date'],
            'numRemision' : idRemission,
            'numCompra' : idCompra
        }        

        registerDelivery(mysql, data)        
            
        urlDetail = '/registro/remission/' + str(idRemission) + '/' + str(idCompra)
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))

@app.route('/newPayment/<idRemission>/<idCompra>', methods = ['POST'] )
def newPayment(idRemission, idCompra):

    user = verifyUser()

    if user[0]:
        data = {
            'user' : user[0],
            'mount' : request.form['mount'],
            'numRemission' : idRemission,
            'numCompra' : idCompra
        }        

        newPaymentF(mysql, data) 
            
        urlDetail = '/registro/remission/' + str(idRemission) + '/' + str(idCompra)
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))

@app.route('/endCommit/<idRemission>/<idCompra>', methods = ['POST'] )
def endommit(idRemission, idCompra):

    user = verifyUser()

    if user[0]:
        data = {
            'accion' : request.form['action'],
            'numRemision' : idRemission,
            'numCompra' : idCompra
        }        

        registerEnd(mysql, data)
        if request.form['origin'] == 'many':
            if request.form['action'] == 'Logistica':
                urlDetail = '/registro/logistics'
            else:
                urlDetail = '/registro/supply'
        else:
            urlDetail = '/registro/remission/' + str(idRemission) + '/' + str(idCompra)
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))

@app.route('/finalizar/<idRemission>/<idCompra>', methods = ['POST'] )
def finalizar(idRemission, idCompra):

    user = verifyUser()

    if user[0]:
        data = {            
            'numRemision' : idRemission,
            'numCompra' : idCompra
        }        

        registerFinalizado(mysql, data)
        if request.form['origin'] == 'many':            
            urlDetail = '/registro/supply'
        else:
            urlDetail = '/registro/remission/' + str(idRemission) + '/' + str(idCompra)
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))

@app.route('/autorizationRC/<idRemission>/<idCompra>', methods = ['POST'] )
def autorizationRC(idRemission, idCompra):

    user = verifyUser()

    if user[0]:
        data = {
            'user' : user[0],
            'numRemision' : idRemission,
            'numCompra' : idCompra
        }        

        updateAutorization(mysql, data)

        urlDetail = ''
        if request.form['origin'] == 'many':
            urlDetail = '/registro/autorizations'
        else:
            urlDetail = '/registro/remission/' + str(idRemission) + '/' + str(idCompra)
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))

@app.route('/addDevolution/<idRemission>/<idCompra>', methods = ['POST'] )
def addDevolution(idRemission, idCompra):

    user = verifyUser()

    if user[0]:
        data = {            
            'numRemision' : idRemission,
            'numCompra' : idCompra,
            'descripcion' : request.form['detail'],
            'cantidadBonificada' : request.form['mount'],
            'resolution' : request.form['resolution']
        }        

        registerDevolution(mysql, data)
        urlDetail = '/registro/remission/' + str(idRemission) + '/' + str(idCompra)
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))

@app.route('/chofer/<idRemission>/<idCompra>', methods = ['POST'] )
def addChofer(idRemission, idCompra):

    user = verifyUser()

    if user[0]:
        data = {
            'numRemision' : idRemission,
            'numCompra' : idCompra,
            'chofer' : request.form['chofer'],            
        }        

        registerChofer(mysql, data)
        urlDetail = '/registro/remission/' + str(idRemission) + '/' + str(idCompra)
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))

@app.route('/confirmPay/<idRemission>/<idCompra>', methods= ['POST'])
def confirmPay(idRemission, idCompra):    
    user = verifyUser()

    if user[0]:
        id = request.form['idUser']
        payment = request.form['idPayment']
        confirmPayment(mysql,  payment, user[0])
        urlDetail = '/registro/remission/' + str(idRemission) + '/' + str(idCompra)
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))
    
@app.route('/noteWeb', methods= ['POST'])
def addNote():
    user = verifyUser()

    if user[0]:
        data = {
            'id' : user[0],
            'content' : request.form['detail'],
            'numRemision' : request.form['numRemision'],
            'numCompra' : request.form['numCompra'],            
            'category' : request.form['category'],
            'idPago' : request.form['idPayment']
        }
        addNoteWeb(mysql, data)

        urlDetail = '/registro/remission/' + str(data['numRemision']) + '/' + str(data['numCompra'])
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))

@app.route('/noteChofer', methods= ['POST'])
def noteChofer():
    user = verifyUser()

    if user[0]:
        data = {
            'id' : user[0],
            'content' : request.form['detail'],
            'numRemision' : request.form['numRemision'],
            'numCompra' : request.form['numCompra'],                        
        }
        addNoteChofer(mysql, data)

        urlDetail = '/registro/remission/' + str(data['numRemision']) + '/' + str(data['numCompra'])
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))

@app.route('/boxes', methods= ['POST'])
def detailBoxes():
    user = verifyUser()

    if user[0]:
        data = {
            'types' : [],
            'cants' : [],
            'nFields' : int(request.form['numFields']),
            'flete' : request.form['fleteval'],
            'numRemision' : request.form['numRemision'],
            'numCompra' : request.form['numCompra']          
        }

        for i in range(1, data['nFields'] + 1 ):
            data['types'].append( request.form['type'+str(i)] )
            data['cants'].append( request.form['cant'+str(i)] )

        addDetailBox(mysql, data)
        urlDetail = '/registro/remission/' + str(data['numRemision']) + '/' + str(data['numCompra'])
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))
@app.route('/uploadExcel', methods= ['POST'])
def uploadExcel():
    user = verifyUser()

    if user[0]:
        file = request.files['excel']
        result = processExcel(mysql, file)
        
        if result == '':
            return redirect(url_for('dashboard'))
        else:
            return render_template('debugUpload.html', msg = result)
    else:
        return redirect(url_for('login'))

#-----------------------------------------------------------------
#api charts

@app.route('/getImportes')
def getImportes():        
    return jsonify( getImportesApi(mysql) )        

@app.route('/getTotalCostumers')
def getTotalCostumers():        
    return jsonify( getTotalCostumersApi(mysql) )        

@app.route('/getRemissionByFilter', methods= ['POST'])
def getRemissionByFilter():
    data = request.get_json()
    return jsonify( getRemissionByApi(mysql, data) )

@app.route('/pdf', methods= ['POST'])
def getPdf():
    data = request.get_json()
    data = getRemissionByApi(mysql, data)['data']
    headers = ['Num Compra', 'Num Remision', 'Fecha', 'Cliente', 'Importe Remisionado', 'Importe Facturado', 'Estatus']
    doc = makePdf(data, headers)
    
    return Response(doc, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers= {"Content-Disposition": "attachment;filename=remisiones.xlsx"} )
#-----------------------------------------------------------------
#post routes android
@app.route('/loginApp', methods= ['POST'])
def postLoginApp():
    data = request.get_json()    
    result = loginApp(mysql, data)
    
    return jsonify( result )

@app.route('/remissionList', methods= ['POST'])
def postRemissionList():
    data = request.get_json()    
    result = choferRemissionList(mysql, data)
    
    return jsonify( result )

@app.route('/remissionListDone', methods= ['POST'])
def postRemissionListDone():
    data = request.get_json()    
    result = choferRemissionListDone(mysql, data)
    
    return jsonify( result )

@app.route('/remissionDetail', methods= ['POST'])
def postRemissionDetail():
    data = request.get_json()    
    result = choferRemissionDetail(mysql, data)
    
    return jsonify( result )

@app.route('/payment', methods= ['POST'])
def postPayment():
    data = request.get_json()    
    result = registerPayment(mysql, data)
    
    return jsonify( result )

@app.route('/note', methods= ['POST'])
def postNote():
    data = request.get_json()    
    result = registerNote(mysql, data)
    
    return jsonify( result )

@app.route('/notePrivate', methods= ['POST'])
def postNotePrivate():
    data = request.get_json()    
    result = getNotesPrivate(mysql, data)
    
    return jsonify( result )

#-------------------------------------------------------------
#routes for costumer site
@app.route('/cliente')
def getMainCostumer():
    return render_template('costumer/login.html')

@app.route('/costumerActiveData', methods= ['POST'])
def costumerActiveData():    
    data = request.get_json()
    result = getCostumerActiveData(mysql, data)
    return jsonify( result )

@app.route('/costumerActiveList', methods= ['POST'])
def costumerActiveList():    
    result = getCostumersActiveData(mysql)
    return jsonify( result )

@app.route('/activateCostumer', methods= ['POST'])
def activateCostumer():    
    data = request.get_json()
    result = activateCostumerF(mysql, data)
    return jsonify( result )

@app.route('/nameCostumerActive', methods= ['POST'])
def nameCostumerActive():    
    data = request.get_json()
    result = getCostumerNameActive(mysql, data)
    return jsonify( result )

@app.route('/loginCostumer', methods= ['POST'])
def postLoginCostumer():    
    data = request.get_json()    
    result = loginCostumer(mysql, data)
    
    if result[1]['result'] == 'failed':
        return jsonify( result[1] )
    else:
        session['costumer_id'] = data['id']
        session['costumer_name'] = result[0]
        return jsonify( result[1] )

@app.route('/changuePSW', methods= ['POST'])
def changuePSW(): 
    user = verifyCostumer()

    if user[0]:   
        data = {
            'clave' : user[0],
            'psw' : request.form['psw']
        }
        result = changuePSWF(mysql, data)
        
        return redirect('/registro/cliente/inicio/active')
    else:
        return redirect(url_for('getMainCostumer'))
@app.route('/cliente/inicio/<status>')
def dashboardCostumer(status):
    user = verifyCostumer()

    if user[0]:
        changuedPSW = verifyPSWCostumer(mysql, user[0])
        if changuedPSW:
            return render_template('costumer/changuePSW.html')
        remissionList = getRemissionsCostumer(mysql,status, user[0] )
        return render_template('costumer/dashboard.html', user = user[1], remissionList = remissionList, active = status, changuedPSW = changuedPSW)
    else:
        return redirect(url_for('getMainCostumer'))

@app.route('/cliente/inicio/remission/<idRemission>/<idCompra>')
def remissionDetailCostumer(idRemission, idCompra):
    user = verifyCostumer()
    if user[0]:
        result = getRemissionDetail(mysql, idRemission, idCompra)
        devolutionDate = verifyYetDevolution(mysql, idRemission, idCompra)         
        
        return render_template('costumer/remissionDetail.html', user = user[1], data = result, devolutionDate = devolutionDate)
    else:
        return redirect(url_for('getMainCostumer'))
    
@app.route('/cliente/addDevolution/<idRemission>/<idCompra>', methods = ['POST'] )
def addDevolutionCostumer(idRemission, idCompra):

    user = verifyUser()

    if user[0]:
        data = {            
            'numRemision' : idRemission,
            'numCompra' : idCompra,
            'descripcion' : request.form['detail'],            
        }        

        registerDevolutioncostumer(mysql, data)
        urlDetail = '/registro/cliente/inicio/remission/' + str(idRemission) + '/' + str(idCompra)
        return redirect(urlDetail)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()