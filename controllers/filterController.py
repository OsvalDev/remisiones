from .chartController import *
from datetime import datetime

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

def getEstatusList(mysql):  
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''SELECT * FROM ESTATUS''')
        data = cur.fetchall()
        
        return {'result':'success', 'data' : data}        

    except Exception as e:
        print(e)
        return {'result':'failed', 'data' : 'Error en la base de datos'}

    finally:
        cur.close()


def getRemissionByApi(mysql, data):
    cur = mysql.connection.cursor()
    
    try:                                

        claves = data.get('costumers', [] )
        statusList = data.get('status', [] )
        dateStart = data.get('dateStart', '')
        dateEnd = data.get('dateEnd', '' )
        nRemision = data.get('numRemision', '')
        nCompra = data.get('numCompra', '')

        params = []
        conditions = []

        if len(claves) > 0:
            placeholders = ', '.join(['%s' for _ in claves])
            conditions.append(f'c.clave IN ({placeholders})')
            params.extend(claves)

        if len(statusList) > 0:
            placeholders = ', '.join(['%s' for _ in statusList])
            conditions.append(f'r.estatus IN ({placeholders})')
            params.extend(statusList)
        
        if dateStart != '' and dateEnd != '':            
            conditions.append('r.fecha >= %s')
            conditions.append('r.fecha <= %s')
            params.append(dateStart)
            params.append(dateEnd)
        
        if nRemision != '':
            conditions.append('r.numRemision LIKE %s')
            params.append(nRemision)

        if nCompra != '':
            conditions.append('r.numCompra LIKE %s')
            params.append(nCompra)
        
        whereClausure = ''

        if len(conditions) > 0:
            whereClausure = 'WHERE ' + ' AND '.join(conditions)

        query = f'''
            SELECT r.numRemision, r.numCompra, r.fecha, c.nombre, e.nombre, r.importeRemisionado, r.importeFacturado
            FROM REMISION AS r
            JOIN CLIENTE AS c ON r.cliente = c.id
            JOIN ESTATUS AS e ON e.id = r.estatus
            {whereClausure}
            ORDER BY r.fecha
        '''

        cur.execute(query, params)        
            
        data = cur.fetchall()
        chartData = getImportesApi(mysql, {'whereClausure' : whereClausure, 'params' : params})
        return {'result':'success', 'data' : data, 'chartData' : chartData}

    except Exception as e:
        print(e)
        return {'result':'failed', 'data' : 'Error en la base de datos'}

    finally:
        cur.close()