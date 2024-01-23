def login(mysql, data):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('SELECT * FROM USUARIO WHERE id = %s and psw = %s and activo = 1', (data['id'], data['psw']) )
        userData = cur.fetchone()

        cur.execute('''
        SELECT DISTINCT p.accion 
        FROM USUARIO AS u
        JOIN USUARIO_AREA AS ua ON u.id = ua.idUsuario
        JOIN AREA AS a ON ua.idArea = a.id
        JOIN AREA_PERMISO AS ap ON ap.idArea = a.id
        JOIN PERMISO AS p ON p.id = ap.idPermiso
        WHERE u.id = %s
        ''', (data['id'], ) )
        privilegiesList = cur.fetchall()
        privilegiesList = [item[0] for item in privilegiesList]        
        if userData != None and privilegiesList != None:
            return [userData[1], {'result' : 'success', 'msg' : 'Ha iniciado sesion correctamente'}, privilegiesList]
        else:
            return [None, {'result' : 'failed', 'msg' : 'Numero de trabajador o contraseña incorrecto'}, None]
    except Exception as e:
        print(e)
        return [None, {'result' : 'failed', 'msg' : 'Error en la conexion con la base de datos'}, None]

    finally:
        cur.close()

def loginApp(mysql, data):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''SELECT u.id FROM USUARIO AS u JOIN USUARIO_AREA AS ua ON u.id = ua.idUsuario
                    JOIN AREA AS a ON a.id = ua.idArea
                    WHERE u.id = %s and u.psw = %s and u.activo = 1 and a.nombre = 'chofer' ''', (data['id'], data['psw']) )
        userData = cur.fetchone()

        if userData != None:
            return {'result' : 'success', 'msg' : 'Ha iniciado sesion correctamente', 'id' : userData[0]}
        else:
            return {'result' : 'failed', 'msg' : 'Numero de trabajador o contraseña incorrecto', 'id' : None}
    except Exception as e:
        print(e)
        return {'result' : 'failed', 'msg' : 'Error en la conexion con la base de datos', 'id' : None}

    finally:
        cur.close()