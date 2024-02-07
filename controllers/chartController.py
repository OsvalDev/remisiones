def getImportesApi(mysql, data=None):
    cur = mysql.connection.cursor()
    try:            
        if data is None:
            cur.execute('''SELECT SUM(importeRemisionado), SUM(importeFacturado) FROM REMISION''')
        else:            
            query = f'''
                SELECT SUM(r.importeRemisionado), SUM(r.importeFacturado)
                FROM REMISION AS r
                JOIN CLIENTE AS c ON r.cliente = c.id
                JOIN ESTATUS AS e ON e.id = r.estatus
                {data['whereClausure']}            
            '''

            cur.execute(query, data['params'])                    
        
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
        cur.execute('''SELECT c.nombre, SUM(r.importeRemisionado + r.importeFacturado) AS totalSuma
                        FROM REMISION AS r
                        JOIN CLIENTE AS c ON r.cliente = c.id
                        GROUP BY c.id
                        ORDER BY totalSuma
                        LIMIT 10;''')            
        data = cur.fetchall()
        
        nombres = [row[0] for row in data]
        total = [row[1] for row in data]
        
        return {'result':'success', 'data' : [nombres, total]}

    except Exception as e:
        print(e)
        return {'result':'failed', 'data' : 'Error en la base de datos'}

    finally:
        cur.close()

