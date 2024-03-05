def registerDateConfirmation (mysql, date, idRemission, idCompra):
    cur = mysql.connection.cursor()

    try:
        cur.execute('UPDATE REMISION SET fechaCompromisoCliente = %s, estatus = 4 WHERE numRemision = %s and numCompra = %s',
                    (date, idRemission, idCompra))
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
                    (data['estatus'], data['numRemision'], data['numCompra']))
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
        cur.execute('''UPDATE PROCESO SET fechaConcluido = current_timestamp() WHERE accion = %s and numRemision = %s and numCompra = %s
                    ''', (data['accion'], data['numRemision'], data['numCompra']))
        mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return {'failed'}

    finally:
        cur.close()

def registerAuditoriaVal (mysql, data):
    cur = mysql.connection.cursor()

    try:
        cur.execute('''INSERT INTO AUDITORIA(numRemision, numCompra, usuario, comentario) VALUES(%s, %s, %s, %s)
                    ''', (data['numRemision'], data['numCompra'], data['user'], data['comentario']))
        mysql.connection.commit()

        cur.execute('''UPDATE REMISION SET estatus = 9 WHERE numRemision = %s and numCompra = %s
                    ''', (data['numRemision'], data['numCompra']))
        mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return False

    finally:
        cur.close()

def updateAutorization (mysql, data):
    cur = mysql.connection.cursor()

    try:
        cur.execute('''UPDATE REMISION SET estatus = 8, autorizador = %s WHERE numRemision = %s and numCompra = %s
                    ''', (data['user'],data['numRemision'], data['numCompra']))
        mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return {'failed'}

    finally:
        cur.close()

def registerFinalizado (mysql, data):
    cur = mysql.connection.cursor()

    try:
        cur.execute('''UPDATE REMISION SET estatus = 7 WHERE numRemision = %s and numCompra = %s
                    ''', (data['numRemision'], data['numCompra']))
        mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return False

    finally:
        cur.close()

def registerDevolution (mysql, data):
    cur = mysql.connection.cursor()

    try:
        cur.execute('''INSERT INTO DEVOLUCION (descripcion, cantidadBonificada, numRemision, numCompra, resolution) VALUES(%s, %s, %s, %s, %s)
                    ''', (data['descripcion'], data['cantidadBonificada'], data['numRemision'], data['numCompra'], data['resolution']))
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


def registerChofer(mysql, data):
    cur = mysql.connection.cursor()

    try:
        cur.execute('SELECT * FROM PROCESO WHERE accion = %s and numRemision = %s and numCompra = %s',
                    ('Entrega',data['numRemision'], data['numCompra']))
        verify = cur.fetchone()

        if verify == None:
            cur.execute('''INSERT INTO PROCESO (accion, numRemision, numCompra, usuario)
                            VALUES (%s, %s, %s, %s )''',
                        ('Entrega', data['numRemision'], data['numCompra'], data['chofer']))
            mysql.connection.commit()

        else:
            cur.execute('''UPDATE PROCESO SET usuario = %s WHERE numRemision = %s and numCompra = %s''',
                        (data['chofer'], data['numRemision'], data['numCompra']))
            mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return {'failed'}
    
    finally:
        cur.close()

def registerDelivery (mysql, data):
    cur = mysql.connection.cursor()

    try:
        cur.execute('''INSERT INTO PROCESO (accion, numRemision, numCompra, usuario, fechaConcluido)
                            VALUES (%s, %s, %s, %s , %s)''',
                        ('Entrega', data['numRemision'], data['numCompra'], data['user'], data['date']))
        mysql.connection.commit()

        cur.execute('''SELECT id FROM PROCESO WHERE accion = %s and numRemision = %s and numCompra = %s''',
                        ('Entrega', data['numRemision'], data['numCompra']))
        idProcess = cur.fetchone()[0]
        
        cur.execute('''INSERT INTO NOTIFICANTEENTREGA VALUES (%s, %s, %s )''',
                    (idProcess, data['user'], data['parcelName']))
        mysql.connection.commit()

        cur.execute('''UPDATE REMISION SET estatus = 5 WHERE numRemision = %s and numCompra = %s''',
                     (data['numRemision'], data['numCompra']))
        mysql.connection.commit()
        
        return True
    except Exception as e:
        print(e)
        return {'failed'}
    
    finally:
        cur.close()

def newPaymentF(mysql, data):
    cur = mysql.connection.cursor()
    try:
        cur.execute('''INSERT INTO PAGO(cantidad, responsable, numRemision, numCompra, confirmante, fechaConfirmacion)
                    VALUES (%s, %s, %s, %s, %s, current_timestamp() )''',
                    ( data['mount'], data['user'], data['numRemission'], data['numCompra'], data['user'] ))
        mysql.connection.commit()        

        cur.execute('''UPDATE REMISION SET estatus = 6 WHERE numRemision = %s and numCompra = %s
            ''', (data['numRemission'], data['numCompra']))
        mysql.connection.commit()
        return {'result' : 'success', 'msg' : 'Pago registrado'}
    except Exception as e:
        print(e)
        return {'result' : 'failed', 'msg' : 'Error en la conexion con la base de datos'}

    finally:
        cur.close()


def confirmPayment (mysql, payment, user):
    cur = mysql.connection.cursor()

    try:
        cur.execute('''UPDATE PAGO SET confirmante = %s, fechaConfirmacion = current_timestamp() WHERE id = %s
                    ''', (user, payment))
        mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return {'failed'}

    finally:
        cur.close()

def addNoteWeb(mysql, data):
    cur = mysql.connection.cursor()                    
    print(data)
    try:
        if data['category'] == 'general':
            print('0')
            cur.execute('''INSERT INTO NOTAREMISION (numRemision, numCompra, contenido, usuario) VALUES (%s, %s, %s, %s)''', (data['numRemision'], data['numCompra'], data['content'], data['id']) )
        elif data['category'] == 'confirmacion':
            print('1')
            cur.execute('''INSERT INTO NOTAENTREGA (numRemision, numCompra, contenido, usuario) VALUES (%s, %s, %s, %s)''', (data['numRemision'], data['numCompra'], data['content'], data['id']) )
        elif data['category'] == 'pago':
            print('2')
            cur.execute('''INSERT INTO NOTAPAGO (id, contenido, usuario) VALUES (%s, %s, %s)''', (data['idPago'], data['content'], data['id']) )
        else:
            print('3')
            cur.execute('''SELECT id FROM PROCESO WHERE numRemision = %s and numCompra = %s and accion = %s''', (data['numRemision'], data['numCompra'], data['category']) )
            idPrroceso = cur.fetchone()[0]
            print(idPrroceso)
            cur.execute('''INSERT INTO NOTA (id, contenido, usuario) VALUES (%s, %s, %s)''', (idPrroceso, data['content'], data['id']) )

        mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return {'failed'}

    finally:
        cur.close()

def addNoteChofer(mysql, data):
    cur = mysql.connection.cursor()                    
    try:
        cur.execute('INSERT INTO NOTAPRIVADA VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s)', (data['numRemision'], data['numCompra'], data['content'], data['id']))
        mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return False

    finally:
        cur.close()

def addDetailBox(mysql, data):
    cur = mysql.connection.cursor()
    print( data )
    try: 
        for i in range(data['nFields']):
            cur.execute('INSERT INTO CAJA VALUES(%s, %s, %s, %s)', (data['numRemision'], data['numCompra'], data['types'][i], int(data['cants'][i])))
            mysql.connection.commit()
        
        cur.execute('UPDATE REMISION SET flete = %s WHERE numRemision = %s and numCompra = %s', (data['flete'], data['numRemision'], data['numCompra']))
        mysql.connection.commit()

        return True    
    except Exception as e:
        print(e)
        return {'failed'}

    finally:
        cur.close()
