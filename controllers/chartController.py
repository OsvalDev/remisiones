def getImportesApi(mysql):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''SELECT SUM(importeRemisionado), SUM(importeFacturado) FROM REMISION''')
        data = cur.fetchone()
        
        return {'result':'success', 'data' : data}        

    except Exception as e:
        print(e)
        return {'result':'failed', 'data' : 'Error en la base de datos'}

    finally:
        cur.close()

def getTotalCostumersApi(mysql):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''SELECT c.nombre, SUM(r.importeRemisionado) AS totalRemisionado, SUM(r.importeFacturado) AS totalFacturado
                        FROM REMISION AS r
                        JOIN CLIENTE AS c ON r.cliente = c.id
                        GROUP BY c.id
                        ORDER BY totalRemisionado DESC, totalFacturado DESC
                        LIMIT 10;''')
        data = cur.fetchall()
        
        nombres = [row[0] for row in data]
        totalRemisionado = [row[1] for row in data]
        
        return {'result':'success', 'data' : [nombres, totalRemisionado]}        

    except Exception as e:
        print(e)
        return {'result':'failed', 'data' : 'Error en la base de datos'}

    finally:
        cur.close()