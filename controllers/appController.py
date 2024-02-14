import base64
from datetime import datetime
import os

def loginApp(mysql, data):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''SELECT u.id FROM USUARIO AS u JOIN USUARIO_AREA AS ua ON u.id = ua.idUsuario
                    JOIN AREA AS a ON a.id = ua.idArea
                    WHERE u.id = %s and u.psw = %s and u.activo = 1 and a.nombre = 'chofer' ''', (data['id'], data['psw']) )
        userData = cur.fetchone()

        if userData != None:
            return {'result' : 'success', 'msg' : 'Ha iniciado sesion correctamente', 'id' : userData[0]}
        else:
            return {'result' : 'failed', 'msg' : 'Numero de trabajador o contraseña invalidos', 'id' : None}
    except Exception as e:
        print(e)
        return {'result' : 'failed', 'msg' : 'Error en la conexion con la base de datos', 'id' : None}

    finally:
        cur.close()

def choferRemissionList(mysql, data):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''                        
                SELECT r.numRemision, r.numCompra, c.nombre, r.importeRemisionado, e.nombre, r.fechaCompromisoCliente
                FROM PROCESO AS p
                JOIN USUARIO AS u ON p.usuario = u.id
                JOIN REMISION AS r ON p.numRemision = r.numRemision and p.numCompra = r.numCompra
                JOIN CLIENTE AS c ON r.cliente = c.id
                JOIN ESTATUS AS e ON  e.id = r.estatus
                WHERE p.accion = 'Entrega' and p.fechaConcluido IS NULL and p.usuario = %s
            ''', (data['id'],))
        remissionList = cur.fetchall()

        if remissionList != None:
            return {'result' : 'success', 'msg' : 'Remisiones asignadas', 'data' : remissionList}
        else:
            return {'result' : 'warning', 'msg' : 'No existen remisiones asignadas', 'data' : remissionList}
    except Exception as e:
        print(e)
        return {'result' : 'failed', 'msg' : 'Error en la conexion con la base de datos', 'data' : None}

    finally:
        cur.close()

def choferRemissionListDone(mysql, data):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''                        
                SELECT r.numRemision, r.numCompra, c.nombre, r.importeRemisionado, e.nombre, r.fechaCompromisoCliente
                FROM PROCESO AS p
                JOIN USUARIO AS u ON p.usuario = u.id
                JOIN REMISION AS r ON p.numRemision = r.numRemision and p.numCompra = r.numCompra
                JOIN CLIENTE AS c ON r.cliente = c.id
                JOIN ESTATUS AS e ON  e.id = r.estatus
                WHERE p.accion = 'Entrega' and p.fechaConcluido IS NOT NULL and p.usuario = %s
            ''', (data['id'],))
        remissionList = cur.fetchall()

        if remissionList != None:
            return {'result' : 'success', 'msg' : 'Remisiones asignadas', 'data' : remissionList}
        else:
            return {'result' : 'warning', 'msg' : 'No existen remisiones asignadas', 'data' : remissionList}
    except Exception as e:
        print(e)
        return {'result' : 'failed', 'msg' : 'Error en la conexion con la base de datos', 'data' : None}

    finally:
        cur.close()

def choferRemissionDetail(mysql, data):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''                        
                SELECT r.numRemision, r.numCompra, c.nombre, r.importeRemisionado, e.nombre, r.fechaCompromisoCliente
                FROM REMISION AS r
                JOIN CLIENTE AS c ON r.cliente = c.id
                JOIN ESTATUS AS e ON  e.id = r.estatus
                WHERE r.numRemision = %s and r.numCompra = %s
            ''', (data['numRemission'], data['numCompra']))
        remission = cur.fetchone()

        if remission != None:
            return {'result' : 'success', 'msg' : 'Informacion de la remision', 'data' : remission}
        else:
            return {'result' : 'warning', 'msg' : 'No existe la remisiones', 'data' : remission}
    except Exception as e:
        print(e)
        return {'result' : 'failed', 'msg' : 'Error en la conexion con la base de datos', 'data' : None}

    finally:
        cur.close()

def registerPayment(mysql, data):

    
    image_data = base64.b64decode(data['img'])
    
    filename = 'payment' + datetime.now().strftime('%Y%m%d%H%M%S') + '.png'
        
    directory = 'static/comprobant/'
    urlImg = os.path.join(directory, filename)
    urlSql = os.path.join("comprobant/", filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(urlImg, 'wb') as f:
        f.write(image_data)
    
    cur = mysql.connection.cursor()
    try:
        cur.execute('''INSERT INTO PAGO(cantidad, pagoPersona, comprobante, responsable, numRemision, numCompra)
                    VALUES (%s, %s, %s, %s, %s, %s)''',
                    (data['cantidad'], data['pagoPersona'], urlSql, data['responsable'], data['numRemission'], data['numCompra'] ))
        mysql.connection.commit()        
        cur.execute('''UPDATE REMISION SET estatus = 5 WHERE numRemision = %s and numCompra = %s
            ''', (data['numRemission'], data['numCompra']))
        mysql.connection.commit()
        return {'result' : 'success', 'msg' : 'Pago registrado'}
    except Exception as e:
        print(e)
        return {'result' : 'failed', 'msg' : 'Error en la conexion con la base de datos'}

    finally:
        cur.close()

def registerNote(mysql, data):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''SELECT id FROM PROCESO WHERE numRemision = %s and numCompra = %s and accion = "Entrega" ''', (data['numRemission'], data['numCompra']) )
        pago = cur.fetchone()

        cur.execute('''INSERT INTO NOTA (id, contenido, usuario) VALUES (%s, %s, %s)''', (pago[0], data['content'], data['id']) )
        mysql.connection.commit()

        return {'result' : 'success', 'msg' : 'Nota registrada'}
    except Exception as e:
        print(e)
        return {'result' : 'failed', 'msg' : 'Error en la conexion con la base de datos'}

    finally:
        cur.close()