from sqlalchemy import text

def syncClientDb(dbSqlServer, mysql):
    try:        
        raw_sql = text('SELECT * FROM CatClientes')
        result = dbSqlServer.session.execute(raw_sql)
        #costumerListSqlServer = [row for row in result]

        # cur = mysql.connection.cursor()        
        # cur.execute('''        
        #     SELECT id
        #     FROM CLIENTE
        # ''' )
        # costumerListMysql = cur.fetchall()        

        # keyCostumers = [key[0] for key in costumerListMysql]
        # inMysql = [row for row in costumerListSqlServer if row[0] in keyCostumers]
        # notInMysql = [row for row in costumerListSqlServer if not row[0] in keyCostumers]
        # modifiedList = [(row[1], row[2], row[0]) for row in inMysql]

        # sqlQuery = "INSERT INTO CLIENTE (id, clave, nombre ) VALUES (%s, %s, %s)"
        # cur.executemany(sqlQuery, notInMysql)
        # mysql.connection.commit()
        
        # sqlQuery = "UPDATE CLIENTE SET clave = %s, nombre = %s WHERE id = %s"
        # cur.executemany(sqlQuery, modifiedList)
        # mysql.connection.commit()
        
        # cur.close()        
        return {'result' : 'success', 'msg' : 'Base de datos sincronizada correctamente'}

    except Exception as e:
        print(e)
        return {'result' : 'failed', 'msg' : 'Error en la base de datos'}
    
def getCostumers(mysql):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT *
            FROM CLIENTE
            ORDER BY saldoBonificado DESC, id
        ''')
        data = cur.fetchall()
        if data != None:
            return data
        else:
            return 'No hay clientes disponibles'

    except Exception as e:
        print(e)
        return 'Error en la base de datos'

    finally:
        cur.close()