def getActiveCostumerList(mysql):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''SELECT DISTINCT nombre, clave FROM CLIENTE AS C JOIN REMISION AS R WHERE C.id = R.cliente''')
        data = cur.fetchall()
        
        return {'result':'success', 'data' : data}        

    except Exception as e:
        print(e)
        return {'result':'failed', 'data' : 'Error en la base de datos'}

    finally:
        cur.close()


def getRemissionByCostumerApi(mysql, clave):
    cur = mysql.connection.cursor()
    print(clave)
    try:                
        cur.execute('''        
            SELECT r.numRemision, r.numCompra, r.fecha, c.nombre, e.nombre
            FROM REMISION AS r
            JOIN CLIENTE AS c ON r.cliente = c.id
            JOIN ESTATUS AS e ON e.id = r.estatus
            WHERE c.clave = %s
            ORDER BY r.numCompra, r.numRemision
        ''', (clave, ))
        data = cur.fetchall()
        return {'result':'success', 'data' : data}

    except Exception as e:
        print(e)
        return {'result':'failed', 'data' : 'Error en la base de datos'}

    finally:
        cur.close()