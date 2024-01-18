import traceback
import pymssql

def syncClientDb(mysql):
    try:                
        conn = pymssql.connect(
                server='p3nwplsk12sql-v17.shr.prod.phx3.secureserver.net:1433',
                user='userp',
                password='oY9u463?e',
                database='dbclientesm',
                as_dict=True
            )        
        
        sqlQuery = 'SELECT * FROM CatClientes'
        cursor = conn.cursor()
        cursor.execute(sqlQuery)        
        costumerListSqlServer = cursor.fetchall()        

        cur = mysql.connection.cursor()
        cur.execute('''        
            SELECT id
            FROM CLIENTE
        ''' )
        costumerListMysql = cur.fetchall()        

        keyCostumers = [key[0] for key in costumerListMysql]
        inMysql = [row for row in costumerListSqlServer if row['Id'] in keyCostumers]
        notInMysql = [row for row in costumerListSqlServer if not row['Id'] in keyCostumers]
        modifiedList = [(row['Clave'], row['Nombre'], row['Id']) for row in inMysql]

        sqlQuery = "INSERT INTO CLIENTE (id, clave, nombre ) VALUES (%s, %s, %s)"
        cur.executemany(sqlQuery, notInMysql)
        mysql.connection.commit()
        
        sqlQuery = "UPDATE CLIENTE SET clave = %s, nombre = %s WHERE id = %s"
        cur.executemany(sqlQuery, modifiedList)
        mysql.connection.commit()
        
        cur.close()        
        return {'result' : 'success', 'msg' : 'Base de datos sincronizada correctamente'}

    except Exception as e:
        print(f"Error details: {e}")
                
        with open("error_log.txt", "a") as log_file:
            log_file.write(traceback.format_exc())
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