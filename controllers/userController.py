def verifyAdmin(mysql, id):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT a.nombre, a.id
            FROM USUARIO AS u 
            JOIN USUARIO_AREA AS ua ON u.id = ua.idUsuario
            JOIN AREA AS a ON ua.idArea = a.id
            WHERE u.id = %s and a.nombre = 'admin'
        ''', (id, ) )
        admin = cur.fetchone()        
        if admin != None:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return 'Error en la base de datos'

    finally:
        cur.close()

def getUsers(mysql, id):
    cur = mysql.connection.cursor()
    try:
        if verifyAdmin(mysql, id):
            cur.execute('''
            SELECT *
            FROM USUARIO AS u 
            JOIN USUARIO_AREA AS ua ON u.id = ua.idUsuario
            JOIN AREA AS a ON ua.idArea = a.id
            ORDER BY u.id
            ''', )
        else:
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
            ORDER BY u.id
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
        if verifyAdmin(mysql, id):
            cur.execute('''        
                SELECT a.nombre, a.id
                FROM AREA AS a
                WHERE a.nombre <> 'gerente'
            ''')
        else:
            cur.execute('''        
                SELECT a.nombre, a.id
                FROM USUARIO AS u 
                JOIN USUARIO_AREA AS ua ON u.id = ua.idUsuario
                JOIN AREA AS a ON ua.idArea = a.id
                WHERE u.id = %s and a.nombre <> 'gerente' and a.nombre <> 'chofer'
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
            INSERT INTO USUARIO(id, nombre, psw) VALUES (%s, %s, %s)
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

def editStatusUser(mysql, id, status):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            UPDATE USUARIO
            SET activo = %s
            WHERE id = %s
        ''', (status, id ) )
        mysql.connection.commit()
        return True

    except Exception as e:
        print(e)
        return 'Error en la base de datos'

    finally:
        cur.close()

def getChoferes(mysql):
    cur = mysql.connection.cursor()
    try:
        cur.execute('''
            SELECT u.id, u.nombre
            FROM USUARIO AS u 
            JOIN USUARIO_AREA AS ua ON u.id = ua.idUsuario
            JOIN AREA AS a ON ua.idArea = a.id
            WHERE a.nombre = 'chofer' and u.activo = 1
            ''', )
        choferList = cur.fetchall()        
        return choferList
    
    except Exception as e:
        print(e)
        return 'Error en la base de datos'

    finally:
        cur.close()
