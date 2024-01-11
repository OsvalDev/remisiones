def getUsers(mysql, id):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''
        SELECT *
        FROM USUARIO AS u 
        JOIN USUARIO_AREA AS ua ON u.id = ua.idUsuario
        JOIN AREA AS a ON ua.idArea = a.id
        WHERE a.nombre IN (
            SELECT a.nombre
            FROM USUARIO AS u 
            JOIN USUARIO_AREA AS ua ON u.id = ua.idUsuario
            JOIN AREA AS a ON ua.idArea = a.id
            WHERE u.id = %s)
        ''', (id, ) )
        userList = cur.fetchall()        
        if userList != None:
            return userList
        else:
            return 'No hay usuarios disponibles'
    except Exception as e:
        print(e)
        return 'Error en la base de datos'

    finally:
        cur.close()

def getAreas(mysql, id):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT a.nombre, a.id
            FROM USUARIO AS u 
            JOIN USUARIO_AREA AS ua ON u.id = ua.idUsuario
            JOIN AREA AS a ON ua.idArea = a.id
            WHERE u.id = %s
        ''', (id, ) )
        areaList = cur.fetchall()        
        if areaList != None:
            return areaList
        else:
            return 'No hay areas disponibles'
    except Exception as e:
        print(e)
        return 'Error en la base de datos'

    finally:
        cur.close()

def addUser(mysql, data):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            INSERT INTO USUARIO VALUES (%s, %s, %s)
        ''', (data[0], data[1], data[2] ) )
        mysql.connection.commit()

        cur.execute('''        
            INSERT INTO USUARIO_AREA(idUsuario, idArea) VALUES (%s, %s)
        ''', (data[0], data[3] ) )
        mysql.connection.commit()

    except Exception as e:
        print(e)
        return 'Error en la base de datos'

    finally:
        cur.close()