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
            return {'result' : 'failed', 'msg' : 'Numero de trabajador o contraseña invalidos', 'id' : None}
    except Exception as e:
        print(e)
        return {'result' : 'failed', 'msg' : 'Error en la conexion con la base de datos', 'id' : None}

    finally:
        cur.close()

def choferRemissionList(mysql, data):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''                        
                SELECT *
                FROM PROCESO AS p
                JOIN USUARIO AS u ON p.usuario = u.id
                JOIN REMISION AS r ON p.numRemision = r.numRemision and p.numCompra = r.numCompra
                WHERE p.accion = 'Entrega' and p.concluido = 0 and p.usuario = %s
            ''', (data['id']))
        remissionList = cur.fetchall()

        if remissionList != None:
            return {'result' : 'success', 'msg' : 'Remisiones asignadas', 'data' : remissionList}
        else:
            return {'result' : 'warning', 'msg' : 'No existen remisiones asignadas', 'data' : remissionList}
    except Exception as e:
        print(e)
        return {'result' : 'failed', 'msg' : 'Error en la conexion con la base de datos', 'data' : None}

    finally:
        cur.close()