def login(mysql, data):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('SELECT * FROM USUARIO WHERE id = %s and psw = %s', (data['id'], data['psw']) )
        userData = cur.fetchone()        
        if userData != None:
            return [userData[1], {'result' : 'success', 'msg' : 'Ha iniciado sesion correctamente'}]
        else:
            return [None, {'result' : 'failed', 'msg' : 'Numero de trabajador o contraseña incorrecto'}]
    except Exception as e:
        print(e)
        return [None, {'result' : 'failed', 'msg' : 'Error en la conexion con la base de datos'}]

    finally:
        cur.close()