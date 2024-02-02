def getImportesApi(mysql, costumer=None):
    cur = mysql.connection.cursor()
    try:
        if costumer is None:
            cur.execute('''SELECT SUM(importeRemisionado), SUM(importeFacturado) FROM REMISION''')
        else:
            cur.execute('''SELECT SUM(importeRemisionado), SUM(importeFacturado) FROM REMISION AS R JOIN CLIENTE AS C ON R.cliente = C.id WHERE C.clave  = %s''', (costumer,))
        
        data = cur.fetchone()
        
        return {'result':'success', 'data' : data}        

    except Exception as e:
        print(e)
        return {'result':'failed', 'data' : 'Error en la base de datos'}

    finally:
        cur.close()

def getTotalCostumersApi(mysql, costumer=None):
    cur = mysql.connection.cursor()
    try:
        if costumer is None:
            cur.execute('''SELECT c.nombre, SUM(r.importeRemisionado) AS totalRemisionado, SUM(r.importeFacturado) AS totalFacturado
                            FROM REMISION AS r
                            JOIN CLIENTE AS c ON r.cliente = c.id
                            GROUP BY c.id
                            ORDER BY totalRemisionado DESC, totalFacturado DESC                        
                            LIMIT 10;''')
        else:
            cur.execute('''SELECT c.nombre, SUM(r.importeRemisionado) AS totalRemisionado, SUM(r.importeFacturado) AS totalFacturado
                            FROM REMISION AS r
                            JOIN CLIENTE AS c ON r.cliente = c.id
                            WHERE c.clave = %s
                            GROUP BY c.id
                            ORDER BY totalRemisionado DESC, totalFacturado DESC                        
                            LIMIT 10;''', (costumer,))
        
        data = cur.fetchall()
        
        nombres = [row[0] for row in data]
        totalRemisionado = [row[1] for row in data]
        totalFacturado = [row[2] for row in data]
        
        return {'result':'success', 'data' : [nombres, totalRemisionado, totalFacturado]}

    except Exception as e:
        print(e)
        return {'result':'failed', 'data' : 'Error en la base de datos'}

    finally:
        cur.close()

