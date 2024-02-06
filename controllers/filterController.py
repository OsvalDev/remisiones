from .chartController import *

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
        chartData = getImportesApi(mysql, data)        
        claves = data['costumers']     
        if len( claves ) > 0:
            placeholders = ', '.join(['%s' for _ in claves])        
            query = f'''
                SELECT r.numRemision, r.numCompra, r.fecha, c.nombre, e.nombre, r.importeRemisionado, r.importeFacturado
                FROM REMISION AS r
                JOIN CLIENTE AS c ON r.cliente = c.id
                JOIN ESTATUS AS e ON e.id = r.estatus
                WHERE c.clave IN ({placeholders})
                ORDER BY r.numCompra, r.numRemision
            '''
            cur.execute(query, claves)
        else:
            cur.execute('''
                SELECT r.numRemision, r.numCompra, r.fecha, c.nombre, e.nombre, r.importeRemisionado, r.importeFacturado
                FROM REMISION AS r
                JOIN CLIENTE AS c ON r.cliente = c.id
                JOIN ESTATUS AS e ON e.id = r.estatus                
                ORDER BY r.numCompra, r.numRemision
            ''')
            
        data = cur.fetchall()
        return {'result':'success', 'data' : data, 'chartData' : chartData}

    except Exception as e:
        print(e)
        return {'result':'failed', 'data' : 'Error en la base de datos'}

    finally:
        cur.close()