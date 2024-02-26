import pandas as pd
import secrets
import string
from datetime import date, datetime, timedelta

def getRemissions(mysql):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT r.numRemision, r.numCompra, r.fecha, c.nombre, e.nombre, r.importeRemisionado, r.importeFacturado
            FROM REMISION AS r
            JOIN CLIENTE AS c ON r.cliente = c.id
            JOIN ESTATUS AS e ON e.id = r.estatus
            ORDER BY r.fecha DESC
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

def getRemissionsCostumer(mysql, active, clave):
    cur = mysql.connection.cursor()
    try:               
        if active == 'active': 
            cur.execute('''        
                SELECT r.numRemision, r.numCompra, r.fecha, c.nombre, e.nombre, r.importeRemisionado, r.importeFacturado
                FROM REMISION AS r
                JOIN CLIENTE AS c ON r.cliente = c.id
                JOIN ESTATUS AS e ON e.id = r.estatus
                WHERE c.clave = %s AND r.estatus <> 7
                ORDER BY r.fecha DESC
            ''', (clave, ))
        else:
            cur.execute('''        
                SELECT r.numRemision, r.numCompra, r.fecha, c.nombre, e.nombre, r.importeRemisionado, r.importeFacturado
                FROM REMISION AS r
                JOIN CLIENTE AS c ON r.cliente = c.id
                JOIN ESTATUS AS e ON e.id = r.estatus
                WHERE c.clave = %s AND r.estatus = 7
                ORDER BY r.fecha DESC
            ''', (clave, ))
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

def getRemissionsByType(mysql, idEstatus, another = False, excludePago = False):
    cur = mysql.connection.cursor()
    try:                
        if excludePago == True:
            cur.execute('''        
                SELECT r.numRemision, r.numCompra, r.fecha, c.nombre, e.nombre, r.importeRemisionado, r.importeFacturado, r.fechaCompromisoCliente  
                FROM REMISION AS r
                JOIN CLIENTE AS c ON r.cliente = c.id
                JOIN ESTATUS AS e ON e.id = r.estatus
                WHERE r.estatus IN (%s, %s)
                AND NOT EXISTS (
                    SELECT 1
                    FROM PAGO AS p
                    WHERE p.numRemision = r.numRemision AND p.numCompra = r.numCompra
                )
                ORDER BY r.fecha DESC;
            ''', (idEstatus, another ))
        else:
            if another == False:
                cur.execute('''        
                    SELECT r.numRemision, r.numCompra, r.fecha, c.nombre, e.nombre, r.importeRemisionado, r.importeFacturado, r.fechaCompromisoCliente
                    FROM REMISION AS r
                    JOIN CLIENTE AS c ON r.cliente = c.id
                    JOIN ESTATUS AS e ON e.id = r.estatus
                    WHERE r.estatus = %s
                    ORDER BY r.fecha DESC
                ''', (idEstatus, ))
            else:
                cur.execute('''        
                    SELECT r.numRemision, r.numCompra, r.fecha, c.nombre, e.nombre, r.importeRemisionado, r.importeFacturado, r.fechaCompromisoCliente  
                    FROM REMISION AS r
                    JOIN CLIENTE AS c ON r.cliente = c.id
                    JOIN ESTATUS AS e ON e.id = r.estatus
                    WHERE r.estatus = %s or r.estatus = %s
                    ORDER BY r.fecha DESC
                ''', (idEstatus, another))
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

def getRemissionsToSupply(mysql):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT r.numRemision, r.numCompra, r.fecha, c.nombre, e.nombre, r.importeRemisionado, r.importeFacturado
            FROM REMISION AS r
            JOIN CLIENTE AS c ON r.cliente = c.id
            JOIN ESTATUS AS e ON e.id = r.estatus
            WHERE r.estatus = 2 or r.estatus = 8
            ORDER BY r.fecha DESC
        ''')
        data = cur.fetchall()
        existDate = []

        if data != None:
            for remission in data:
                cur.execute('SELECT fechaConcluido FROM PROCESO WHERE accion = "Surtimiento" and numRemision = %s and numCompra = %s', (remission[0], remission[1]))
                exist = cur.fetchone()
                print(exist)
                if exist != None:
                    existDate.append([True, exist[0]])
                else:
                    existDate.append([False, ''])
            return [data, existDate]
        else:
            return 'No hay remisiones disponibles'

    except Exception as e:
        print(e)
        return 'Error en la base de datos'

    finally:
        cur.close()

def getRemissionsToLogistic(mysql):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT r.numRemision, r.numCompra, r.fecha, c.nombre, e.nombre, r.importeRemisionado, r.importeFacturado
            FROM REMISION AS r
            JOIN CLIENTE AS c ON r.cliente = c.id
            JOIN ESTATUS AS e ON e.id = r.estatus
            WHERE r.estatus = 2 or r.estatus = 3 or r.estatus = 4
            ORDER BY r.fecha DESC
        ''')
        data = cur.fetchall()
        existDate = []        
        
        if data != None:
            for remission in data:
                cur.execute('SELECT fechaConcluido FROM PROCESO WHERE accion = "Logistica" and numRemision = %s and numCompra = %s', (remission[0], remission[1]))
                exist = cur.fetchone()                
                if exist != None:
                    existDate.append([True, exist[0]])
                else:
                    existDate.append([False, ''])            
            return [data, existDate]
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

def getCostumerNameActive(mysql, data):
    value = data['numCliente']
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT nombre, saldoBonificado
            FROM CLIENTE
            WHERE clave = %s AND id NOT IN (SELECT id
                                            FROM CLIENTE_SITIO )
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

def activateCostumerF(mysql, data):
    value = data['numCliente']
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT id
            FROM CLIENTE
            WHERE clave = %s
        ''', (value, ))
        idCostumer = cur.fetchone()

        longitud = 6
        caracteres = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(caracteres) for _ in range(longitud))
        
        if data != None:
            cur.execute('INSERT INTO CLIENTE_SITIO(id, psw) VALUES (%s, %s)', (idCostumer[0], token ))
            mysql.connection.commit()

            return {'result':'success'}
        else:
            return {'result':'failed'}

    except Exception as e:
        print(e)
        return {'result':'failed'}

    finally:
        cur.close()

def getCostumerActiveData(mysql, data):
    value = data['numCliente']
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT c.nombre, s.psw
            FROM CLIENTE AS c 
            NATURAL JOIN CLIENTE_SITIO AS s
            WHERE clave = %s AND bringPsw = 1
        ''', (value, ))
        data = cur.fetchone()
        if data != None:
            return {'result':'success'}
        else:
            return {'result':'failed'}

    except Exception as e:
        print(e)
        return {'result':'failed'}

    finally:
        cur.close()

def getCostumersActiveData(mysql):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT c.nombre, s.psw
            FROM CLIENTE AS c 
            NATURAL JOIN CLIENTE_SITIO AS s
            WHERE bringPsw = 1
        ''')
        data = cur.fetchall()
        if len(data) > 0:
            return {'result':'success', 'data' : data}
        else:
            return {'result':'failed'}

    except Exception as e:
        print(e)
        return {'result':'failed'}

    finally:
        cur.close()

def verifyYetDevolution(mysql, numRemision, numCompra):
    cur = mysql.connection.cursor()
    try:            
        cur.execute('SELECT fechaConcluido FROM PROCESO WHERE accion = "Entrega" and numRemision = %s and numCompra = %s', (numRemision, numCompra))
        fecha_mysql = cur.fetchone()[0]
        fecha_mysql = datetime.strptime(str(fecha_mysql), "%Y-%m-%d").date()
        
        fecha_actual = date.today()    
        fecha_limite = fecha_actual + timedelta(days=2)
        
        if fecha_mysql <= fecha_actual <= fecha_limite:
            return [True, fecha_mysql, fecha_limite]
        else:
            return [False, fecha_mysql, fecha_limite]
    except Exception as e:
        print(e)
        return False

    finally:
        cur.close()
def addRemission(mysql, data):    
    cur = mysql.connection.cursor()
    try:                
        numRemission = data['numRemission'].replace(' ', '_')
        numCompra = data['numCompra'].replace(' ', '_')
        cur.execute('''        
            SELECT id, saldoBonificado
            FROM CLIENTE
            WHERE clave = %s
        ''', (data['numCliente'], ))
        costumerid = cur.fetchone()        
        cur.execute('''        
            INSERT INTO REMISION (numRemision, numCompra, piezas, importeRemisionado, importeFacturado, cliente, saldoAFavor, numFactura)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (numRemission,numCompra , data['piezas'], data['remisionado'], data['facturado'], costumerid[0], data['bonificado'], data['factura'] ))
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
        'autorizante' : None,
        'surtimiento' : None,
        'logistica' : None,
        'confirmacionEntrega' : None,
        'pagos' : None,
        'devoluciones' : None,
        'chofer' : None,
        'parcelDelivery' : None,
        'baseComment' : None,
        'surtimientoComment' : None,
        'logisticaComment' : None,
        'registroComment' : None,        
        'notasPagos' : None,       
        'boxes' : None,
        'solicitud' : None
    }
    
    cur = mysql.connection.cursor()

    try:
        cur.execute('''        
            SELECT r.numRemision, r.numCompra, c.nombre, r.piezas, r.importeFacturado, r.importeRemisionado, r.saldoAFavor, r.fecha, c.clave, r.numFactura, r.estatus, r.autorizador, r.flete
            FROM REMISION AS r
            JOIN CLIENTE AS c ON r.cliente = c.id
            WHERE r.numRemision = %s and r.numCompra = %s
        ''', (numRemision, numCompra))
        data['baseData'] = cur.fetchone()

        if data['baseData']:
            #autorizante
            if data['baseData'][11] != None:
                cur.execute('''SELECT nombre
                                FROM USUARIO
                                WHERE id = %s
                            ''', (data['baseData'][11],))
                data['autorizante'] = cur.fetchone()[0]
            #base comment
            cur.execute('''        
                SELECT u.nombre, N.fecha, N.contenido
                FROM REMISION AS R
                JOIN NOTAREMISION AS N ON R.numRemision = N.numRemision and R.numCompra = N.numCompra 
                JOIN USUARIO AS u on u.id = N.usuario
                WHERE R.numRemision = %s and R.numCompra = %s
            ''', (numRemision, numCompra))
            data['baseComment'] = cur.fetchall()

            #surtimiento
            cur.execute('''                        
                SELECT p.fechaCompromiso, p.fechaConcluido, u.nombre, p.fecha
                FROM PROCESO AS p
                JOIN USUARIO AS u ON p.usuario = u.id
                WHERE p.numRemision = %s and p.numCompra = %s and p.accion = 'Surtimiento'
            ''', (numRemision, numCompra))
            data['surtimiento'] = cur.fetchone()
            #notas surtimiento
            cur.execute('''        
                SELECT u.nombre, NP.fecha, NP.contenido
                FROM PROCESO AS P
                JOIN NOTA AS NP ON P.id = NP.id 
                JOIN USUARIO AS u on u.id = NP.usuario
                WHERE P.numRemision = %s and P.numCompra = %s and P.accion = "Surtimiento"
            ''', (numRemision, numCompra))
            data['surtimientoComment'] = cur.fetchall()
            
            #logistica
            cur.execute('''                        
                SELECT p.fechaCompromiso, p.fechaConcluido, u.nombre, p.fecha
                FROM PROCESO AS p
                JOIN USUARIO AS u ON p.usuario = u.id
                WHERE p.numRemision = %s and p.numCompra = %s and p.accion = 'Logistica'
            ''', (numRemision, numCompra))
            data['logistica'] = cur.fetchone()
            #chofer
            cur.execute('''                        
                SELECT u.nombre
                FROM PROCESO AS p
                JOIN USUARIO AS u ON p.usuario = u.id
                WHERE p.numRemision = %s and p.numCompra = %s and p.accion = 'Entrega'
            ''', (numRemision, numCompra))
            data['chofer'] = cur.fetchone()

            cur.execute('''                        
                SELECT u.nombre, n.paqueteria, p.fechaConcluido
                FROM PROCESO AS p
                JOIN NOTIFICANTEENTREGA AS n ON p.id = n.id
                JOIN USUARIO AS u ON u.id = n.usuario
                WHERE p.numRemision = %s and p.numCompra = %s and p.accion = 'Entrega'
            ''', (numRemision, numCompra))
            data['parcelDelivery'] = cur.fetchone()

            #notas logistica
            cur.execute('''        
                SELECT u.nombre, NP.fecha, NP.contenido
                FROM PROCESO AS P
                JOIN NOTA AS NP ON P.id = NP.id 
                JOIN USUARIO AS u on u.id = NP.usuario
                WHERE P.numRemision = %s and P.numCompra = %s and P.accion = "Logistica"
            ''', (numRemision, numCompra))
            data['logisticaComment'] = cur.fetchall()
            #confirmacionEntrega
            cur.execute('''        
                SELECT r.fechaCompromisocliente
                FROM REMISION AS r                
                WHERE r.numRemision = %s and r.numCompra = %s
            ''', (numRemision, numCompra))
            data['confirmacionEntrega'] = cur.fetchone()
            #base comment
            cur.execute('''        
                SELECT u.nombre, N.fecha, N.contenido
                FROM REMISION AS R
                JOIN NOTAENTREGA AS N ON R.numRemision = N.numRemision and R.numCompra = N.numCompra 
                JOIN USUARIO AS u on u.id = N.usuario
                WHERE R.numRemision = %s and R.numCompra = %s
            ''', (numRemision, numCompra))
            data['registroComment'] = cur.fetchall()
            #pagos
            cur.execute('''        
                SELECT P.id, P.cantidad, P.pagoPersona, P.fecha, U.nombre, P.comprobante, Us.nombre, P.fechaConfirmacion, P.entregasrc, P.identificacionsrc, P.calidadval, P.cantidadval
                FROM PAGO AS P
                JOIN USUARIO AS U ON U.id = P.responsable
                LEFT JOIN USUARIO AS Us ON Us.id = P.confirmante
                WHERE P.numRemision = %s and P.numCompra = %s
            ''', (numRemision, numCompra))
            data['pagos'] = cur.fetchall()

            #notas by pago
            i = 0
            aux = []
            for pago in data['pagos']:
                # Convertir el elemento de la tupla a una lista
                pago_lista = list(pago)
                
                cur.execute('''
                    SELECT u.nombre, NP.fecha, NP.contenido
                    FROM NOTAPAGO AS NP
                    JOIN USUARIO AS u on u.id = NP.usuario
                    WHERE NP.id = %s
                ''', (pago[0],))
                
                # Agregar la información adicional a la lista
                pago_lista.append(cur.fetchall())
                
                # Convertir la lista de nuevo a una tupla si es necesario
                aux.append( tuple(pago_lista) )
                
                i += 1
            data['pagos'] = aux

            #notas pagos
            cur.execute('''        
                SELECT u.nombre, NP.fecha, NP.contenido
                FROM PROCESO AS P
                JOIN NOTA AS NP ON P.id = NP.id 
                JOIN USUARIO AS u on u.id = NP.usuario
                WHERE P.numRemision = %s and P.numCompra = %s and P.accion = "Entrega"
            ''', (numRemision, numCompra))
            data['notasPagos'] = cur.fetchall()

            #devoluciones
            cur.execute('''                        
                SELECT D.descripcion, D.cantidadBonificada, D.fecha, D.resolution
                FROM DEVOLUCION AS D
                WHERE D.numRemision = %s and D.numCompra = %s
            ''', (numRemision, numCompra))
            data['devoluciones'] = cur.fetchall()

            #cajas logisitca
            cur.execute('SELECT tipo, cantidad FROM CAJA WHERE numRemision = %s and numCompra = %s',
                        (numRemision, numCompra))
            data['boxes'] = cur.fetchall()

            #solicitud devolucion
            cur.execute('SELECT detalle FROM SOLICITUD WHERE numRemision = %s and numCompra = %s',
                        (numRemision, numCompra))
            data['solicitud'] = cur.fetchone()
            
            return data
        
        else:
            return {'result': 'failed'}
            
    except Exception as e:
        print(e)
        return {'result': 'failed'}
    
    finally:
        cur.close()

def processExcel(mysql, file):
    resultingMsg = ''
    try:
        df = pd.read_excel(file)

        for index, row in df.iterrows():                        

            #validar datos
            if pd.isnull(row['Numero de compra']):
                resultingMsg +=f"Numero de compra incompleto en la fila {index + 2}. </br>"
                continue
            if pd.isnull(row['Numero de remision']):
                resultingMsg +=f"Numero de remision incompleto en la fila {index + 2}. </br>"
                continue
            if pd.isnull(row['Numero de factura']):
                resultingMsg +=f"Numero de factura incompleto en la fila {index + 2}. </br>"
                continue
            if pd.isnull(row['Clave del cliente']):
                resultingMsg +=f"Clave del cliente incompleto en la fila {index + 2}. </br>"
                continue
            if pd.isnull(row['Piezas']):
                resultingMsg +=f"Piezas incompleto en la fila {index + 2}. </br>"
                continue
            if pd.isnull(row['Importe remisionado']):
                resultingMsg +=f"Importe remisionado incompleto en la fila {index + 2}. </br>"
                continue
            if pd.isnull(row['Importe facturado']):
                resultingMsg +=f"Importe facturado incompleto en la fila {index + 2}. </br>"
                continue
            if pd.isnull(row['Monto bonificado']):
                resultingMsg +=f"Monto bonificado incompleto en la fila {index + 2}. </br>"
                continue

            # Verifica que los valores numéricos sean válidos
            try:
                piezas = int(row['Piezas'])                
            except ValueError:
                resultingMsg +=f"El valor de piezas no es numerico en la fila {index + 2}.</br>"
                continue
            try:                
                remisionado = float(row['Importe remisionado'])                
            except ValueError:
                resultingMsg +=f"El valor de importe remisionado no es numerico en la fila {index + 2}.</br>"
                continue
            try:                
                facturado = float(row['Importe facturado'])                
            except ValueError:
                resultingMsg +=f"El valor de importe facturado no es numerico en la fila {index + 2}.</br>"
                continue
            try:                
                bonificado = float(row['Monto bonificado'])
            except ValueError:
                resultingMsg +=f"El valor de monto bonificado no es numerico en la fila {index + 2}.</br>"
                continue
            
            numRemission = row['Numero de remision'].replace(' ', '_')
            numCompra = row['Numero de compra'].replace(' ', '_')
            cur = mysql.connection.cursor()
            #No existe otra remision con el mismo numero de remision y numero de compra
            cur.execute('SELECT * FROM REMISION WHERE numRemision = %s and numCompra = %s', (numRemission, numCompra))
            auxTest = cur.fetchone()
            if auxTest:
                resultingMsg += f"La remision { numRemission } con # de compra { numCompra } ya existe en la fila {index + 2}. </br>"
                continue

            #la clave del cliente existe
            cur.execute('SELECT saldoBonificado FROM CLIENTE WHERE clave = %s', (row['Clave del cliente'], ))
            auxTest = cur.fetchone()
            if auxTest is None:
                resultingMsg += f"La clave del cliente en la fila {index + 2} no existe. </br>"
                continue
            
            if float(auxTest[0]) < row['Monto bonificado']:
                resultingMsg += f"El saldo del cliente en la fila {index + 2} no es suficiente para la bonificacion. </br>"
                continue


            # #ingresar el registro
            cur.execute('''        
                SELECT id, saldoBonificado
                FROM CLIENTE
                WHERE clave = %s
            ''', (row['Clave del cliente'], ))
            costumerid = cur.fetchone()

            # Inserta la nueva remisión en la base de datos            
            cur.execute('''        
                INSERT INTO REMISION (numRemision, numCompra, piezas, importeRemisionado, importeFacturado, cliente, saldoAFavor, numFactura)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (numRemission, numCompra, row['Piezas'], row['Importe remisionado'], row['Importe facturado'], costumerid[0], row['Monto bonificado'], row['Numero de factura'] ))
            mysql.connection.commit()

            # Actualiza el saldoBonificado del cliente si es necesario
            if row['Monto bonificado'] != '' and int(row['Monto bonificado']) > 0:
                mount = int(row['Monto bonificado'])
                balance = int(costumerid[1])
                
                cur.execute('UPDATE CLIENTE SET saldoBonificado = %s WHERE id = %s', (balance - mount, costumerid[0]))
                mysql.connection.commit()
            
        
        return resultingMsg

    except Exception as e:
        print(f"Error processing Excel file: {e}")
        return False
    