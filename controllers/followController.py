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

    try:
        if data['category'] in ['general', 'confirmacion']:
            cur.execute('''INSERT INTO NOTAREMISION (numRemision, numCompra, contenido, usuario) VALUES (%s, %s, %s, %s)''', (data['numRemision'], data['numCompra'], data['content'], data['id']) )
        elif data['category'] == 'pago':
            cur.execute('''INSERT INTO NOTAPAGO (id, contenido, usuario) VALUES (%s, %s, %s)''', (data['idCategory'], data['content'], data['id']) )
        else:
            cur.execute('''SELECT id FROM PROCESO WHERE numRemision = %s and numCompra = %s and accion = %s''', (data['numRemission'], data['numCompra'], data['category']) )
            idPrroceso = cur.fetchone()[0]
            cur.execute('''INSERT INTO NOTA (id, contenido, usuario) VALUES (%s, %s, %s)''', (idPrroceso, data['content'], data['id']) )

        mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return {'failed'}

    finally:
        cur.close()
