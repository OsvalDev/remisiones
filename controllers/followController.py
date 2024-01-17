def registerDateConfirmation (mysql, date, idRemission, idCompra):
    cur = mysql.connection.cursor()

    try:
        cur.execute('UPDATE REMISION SET fechaCompromisoCliente = %s WHERE numRemision = %s and numCompra = %s',
                    (date, idRemission, idCompra))
        mysql.connection.commit()

        return True
    except Exception as e:
        print(e)
        return {'failed'}
    
    finally:
        cur.close()