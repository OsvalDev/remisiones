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