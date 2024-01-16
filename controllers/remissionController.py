def getRemissions(mysql):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT r.numRemision, r.numCompra, r.fecha, c.nombre, r.estatus
            FROM REMISION AS r
            JOIN CLIENTE AS c ON r.cliente = c.id
        ''')
        data = cur.fetchall()
        if data != None:
            return data
        else:
            return 'No hay remisiones disponibles'

    except Exception as e:
        print(e)
        return 'Error en la base de datos'

    finally:
        cur.close()

def getCostumerName(mysql, data):
    value = data['numCliente']
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT nombre
            FROM CLIENTE
            WHERE clave = %s
        ''', (value, ))
        data = cur.fetchone()
        if data != None:
            return {'result':'success', 'name' : data[0]}
        else:
            return {'result':'success', 'name' : 'Cliente no encontrado'}

    except Exception as e:
        print(e)
        return {'result':'failed'}

    finally:
        cur.close()

def addRemission(mysql, data):    
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT id
            FROM CLIENTE
            WHERE clave = %s
        ''', (data['numCliente'], ))
        costumerid = cur.fetchone()

        cur.execute('''        
            INSERT INTO REMISION (numRemision, numCompra, piezas, importeRemisionado, importeFacturado, cliente)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (data['numCompra'], data['numRemission'], data['piezas'], data['remisionado'], data['facturado'], costumerid ))
        mysql.connection.commit()

    except Exception as e:
        print(e)
        return {'result':'failed'}

    finally:
        cur.close()

def getRemissionDetail(mysql, numRemision, numCompra):
    data = {
        'baseData' : None,
        'surtimiento' : None,
        'logistica' : None,
        'confirmacionEntrega' : None,
        'pagos' : None,
        'confirmacionPagos' : None,
        'devoluciones' : None
    }
    
    cur = mysql.connection.cursor()

    try:
        cur.execute('''        
            SELECT r.numRemision, r.numCompra, c.nombre, r.piezas, r.importeFacturado, r.importeRemisionado, r.saldoAFavor
            FROM REMISION AS r
            JOIN CLIENTE AS c ON r.cliente = c.id
            WHERE r.numRemision = %s and r.numCompra = %s
        ''', (numRemision, numCompra))
        data['baseData'] = cur.fetchone()

        if data['baseData']:
            #surtimiento
            cur.execute('''                        
                SELECT p.fechaCompromiso, p.concluido, u.nombre, p.fecha
                FROM PROCESO AS p
                JOIN USUARIO AS u ON p.usuario = u.id
                WHERE p.numRemision = %s and p.numCompra = %s and p.accion = 'Surtimiento'
            ''', (numRemision, numCompra))
            data['surtimiento'] = cur.fetchone()
            
            #logistica
            cur.execute('''                        
                SELECT p.fechaCompromiso, p.concluido, u.nombre, p.fecha
                FROM PROCESO AS p
                JOIN USUARIO AS u ON p.usuario = u.id
                WHERE p.numRemision = %s and p.numCompra = %s and p.accion = 'Logistica'
            ''', (numRemision, numCompra))
            data['logistica'] = cur.fetchone()

            #confirmacionEntrega
            cur.execute('''        
                SELECT r.fechaCompromisocliente
                FROM REMISION AS r                
                WHERE r.numRemision = %s and r.numCompra = %s
            ''', (numRemision, numCompra))
            data['confirmacionEntrega'] = cur.fetchone()

            return data
        
        else:
            return {'result': 'failed'}
            
    except Exception as e:
        print(e)
        return {'result': 'failed'}
    
    finally:
        cur.close()