def getRemissions(mysql):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT r.numRemision, r.numCompra, r.fecha, c.nombre, r.estatus
            FROM REMISION AS r
            JOIN CLIENTE AS c ON r.cliente = c.id
            ORDER BY r.numCompra, r.numRemision
        ''')
        data = cur.fetchall()
        if data != None:
            return data
        else:
            return 'No hay remisiones disponibles'

    except Exception as e:
        print(e)
        return 'Error en la base de datos'

    finally:
        cur.close()

def getCostumerName(mysql, data):
    value = data['numCliente']
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT nombre, saldoBonificado
            FROM CLIENTE
            WHERE clave = %s
        ''', (value, ))
        data = cur.fetchone()
        if data != None:
            return {'result':'success', 'name' : data[0], 'saldo' : data[1]}
        else:
            return {'result':'success', 'name' : 'Cliente no encontrado', 'saldo' : 0}

    except Exception as e:
        print(e)
        return {'result':'failed'}

    finally:
        cur.close()

def addRemission(mysql, data):    
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT id, saldoBonificado
            FROM CLIENTE
            WHERE clave = %s
        ''', (data['numCliente'], ))
        costumerid = cur.fetchone()        
        cur.execute('''        
            INSERT INTO REMISION (numRemision, numCompra, piezas, importeRemisionado, importeFacturado, cliente, saldoAFavor, numFactura)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (data['numRemission'], data['numCompra'], data['piezas'], data['remisionado'], data['facturado'], costumerid[0], data['bonificado'], data['factura'] ))
        mysql.connection.commit()

        if data['bonificado'] != '' and int(data['bonificado']) > 0:
            mount = int(data['bonificado'])
            balance =  int(costumerid[1])
            
            cur.execute('UPDATE CLIENTE SET saldoBonificado = %s WHERE id = %s', (balance-mount, costumerid[0]))
            mysql.connection.commit()

        return {'result' : 'success'}

    except Exception as e:
        print(e)
        return {'result':'failed'}

    finally:
        cur.close()

def changueRemission(mysql, data):    
    cur = mysql.connection.cursor()
    try:             
        cur.execute('''        
            SELECT id, saldoBonificado
            FROM CLIENTE
            WHERE id = (
                    SELECT cliente
                    FROM REMISION
                    WHERE numRemision = %s and numCompra = %s
            )
        ''', ( data['numRemision'], data['numCompra'] ))
        saldoBonificado = cur.fetchone()

        if data['saldoInicial'] != data['saldoAFavor']:
            initialCurrency = float(data['saldoInicial'])
            newBonify = float(data['saldoAFavor'])

            if initialCurrency < newBonify:
                total = newBonify - initialCurrency
                newActual = saldoBonificado[1] - total
                if newActual >=0:
                    cur.execute('UPDATE CLIENTE SET saldoBonificado = %s WHERE id = %s', (newActual, saldoBonificado[0]))
                    mysql.connection.commit()
                else:
                    return {'result':'failed', 'msg' : 'Saldo insuficiente'}
            else:
                total = initialCurrency - newBonify
                newActual = saldoBonificado[1] + total
                cur.execute('UPDATE CLIENTE SET saldoBonificado = %s WHERE id = %s', (newActual, saldoBonificado[0]))
                mysql.connection.commit()

        cur.execute('''        
            UPDATE REMISION SET piezas = %s, importeRemisionado = %s, importeFacturado = %s, saldoAFavor = %s, numFactura = %s
            WHERE numRemision = %s and numCompra = %s
        ''', ( data['piezas'], data['remisionado'], data['facturado'],data['saldoAFavor'], data['numFactura'], data['numRemision'], data['numCompra'] ))
        mysql.connection.commit()

        return {'result' : 'success'}

    except Exception as e:
        print(e)
        return {'result':'failed'}

    finally:
        cur.close()

def getRemissionDetail(mysql, numRemision, numCompra):
    data = {
        'baseData' : None,
        'surtimiento' : None,
        'logistica' : None,
        'confirmacionEntrega' : None,
        'pagos' : None,
        'notasPagos' : None,
        'devoluciones' : None,
        'chofer' : None
    }
    
    cur = mysql.connection.cursor()

    try:
        cur.execute('''        
            SELECT r.numRemision, r.numCompra, c.nombre, r.piezas, r.importeFacturado, r.importeRemisionado, r.saldoAFavor, r.fecha, c.clave, r.numFactura
            FROM REMISION AS r
            JOIN CLIENTE AS c ON r.cliente = c.id
            WHERE r.numRemision = %s and r.numCompra = %s
        ''', (numRemision, numCompra))
        data['baseData'] = cur.fetchone()

        if data['baseData']:
            #surtimiento
            cur.execute('''                        
                SELECT p.fechaCompromiso, p.fechaConcluido, u.nombre, p.fecha
                FROM PROCESO AS p
                JOIN USUARIO AS u ON p.usuario = u.id
                WHERE p.numRemision = %s and p.numCompra = %s and p.accion = 'Surtimiento'
            ''', (numRemision, numCompra))
            data['surtimiento'] = cur.fetchone()
            
            #logistica
            cur.execute('''                        
                SELECT p.fechaCompromiso, p.fechaConcluido, u.nombre, p.fecha
                FROM PROCESO AS p
                JOIN USUARIO AS u ON p.usuario = u.id
                WHERE p.numRemision = %s and p.numCompra = %s and p.accion = 'Logistica'
            ''', (numRemision, numCompra))
            data['logistica'] = cur.fetchone()
            
            cur.execute('''                        
                SELECT u.nombre
                FROM PROCESO AS p
                JOIN USUARIO AS u ON p.usuario = u.id
                WHERE p.numRemision = %s and p.numCompra = %s and p.accion = 'Entrega'
            ''', (numRemision, numCompra))
            data['chofer'] = cur.fetchone()

            #confirmacionEntrega
            cur.execute('''        
                SELECT r.fechaCompromisocliente
                FROM REMISION AS r                
                WHERE r.numRemision = %s and r.numCompra = %s
            ''', (numRemision, numCompra))
            data['confirmacionEntrega'] = cur.fetchone()

            #pagos
            cur.execute('''        
                SELECT P.id, P.cantidad, P.pagoPersona, P.fecha, U.nombre, P.comprobante, P.confirmante, P.fechaConfirmacion
                FROM PAGO AS P
                JOIN USUARIO AS U ON U.id = P.responsable 
                WHERE P.numRemision = %s and P.numCompra = %s
            ''', (numRemision, numCompra))
            data['pagos'] = cur.fetchall()                                                

            cur.execute('''        
                SELECT NP.usuario, NP.fecha, NP.contenido
                FROM PAGO AS P
                JOIN NOTA AS NP ON P.id = NP.id 
                WHERE P.numRemision = %s and P.numCompra = %s
            ''', (numRemision, numCompra))
            data['notasPagos'] = cur.fetchall()

            #surtimiento
            cur.execute('''                        
                SELECT D.descripcion, D.cantidadBonificada, D.fecha
                FROM DEVOLUCION AS D
                WHERE D.numRemision = %s and D.numCompra = %s
            ''', (numRemision, numCompra))
            data['devoluciones'] = cur.fetchall()            

            return data
        
        else:
            return {'result': 'failed'}
            
    except Exception as e:
        print(e)
        return {'result': 'failed'}
    
    finally:
        cur.close()