def registerDateConfirmation (mysql, date, idRemission, idCompra):
    cur = mysql.connection.cursor()

    try:
        cur.execute('UPDATE REMISION SET fechaCompromisoCliente = %s WHERE numRemision = %s and numCompra = %s',
                    (date, idRemission, idCompra))
        mysql.connection.commit()

        cur.execute('UPDATE REMISION SET estatus = "Entrega confirmada" WHERE numRemision = %s and numCompra = %s',
                    (idRemission, idCompra))
        mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return {'failed'}
    
    finally:
        cur.close()

def registerDateCommit (mysql, data):
    cur = mysql.connection.cursor()

    try:
        cur.execute('''INSERT INTO PROCESO (accion, fechaCompromiso, numRemision, numCompra, usuario)
                        VALUES (%s, %s, %s, %s, %s )''',
                    (data['accion'], data['fechaCompromiso'], data['numRemision'], data['numCompra'], data['usuario']))
        mysql.connection.commit()

        cur.execute('UPDATE REMISION SET estatus = %s WHERE numRemision = %s and numCompra = %s',
                    (data['accion'], data['numRemision'], data['numCompra']))
        mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return {'failed'}
    
    finally:
        cur.close()

def registerEnd (mysql, data):
    cur = mysql.connection.cursor()

    try:
        cur.execute('''UPDATE PROCESO SET concluido = 1 WHERE accion = %s and numRemision = %s and numCompra = %s
                    ''', (data['accion'], data['numRemision'], data['numCompra']))
        mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return {'failed'}

    finally:
        cur.close()

def registerDevolution (mysql, data):
    cur = mysql.connection.cursor()

    try:
        cur.execute('''INSERT INTO DEVOLUCION (descripcion, cantidadBonificada, numRemision, numCompra) VALUES(%s, %s, %s, %s)
                    ''', (data['descripcion'], data['cantidadBonificada'], data['numRemision'], data['numCompra']))
        mysql.connection.commit()

        cur.execute('''SELECT saldoBonificado, id FROM CLIENTE WHERE id = (
                                                SELECT cliente FROM REMISION WHERE numRemision = %s and numCompra = %s)'''
                    , (data['numRemision'], data['numCompra']))
        currentCurrency =  cur.fetchone()
        
        totalCurrency = currentCurrency[0] + int(data['cantidadBonificada'])        

        cur.execute('UPDATE CLIENTE SET saldoBonificado = %s WHERE id = %s', (totalCurrency,currentCurrency[1]))
        mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return {'failed'}

    finally:
        cur.close()