def verifyPSWCostumer (mysql, clave):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            SELECT *
            FROM CLIENTE_SITIO
            NATURAL JOIN CLIENTE
            WHERE clave = %s AND bringPsw = 0
        ''', (clave, ) )
        changued = cur.fetchone()        
        if changued != None:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return 'Error en la base de datos'

    finally:
        cur.close()

def changuePSWF (mysql, data):
    cur = mysql.connection.cursor()
    try:                
        cur.execute('''        
            UPDATE CLIENTE_SITIO SET bringPSW = 0, psw = %s            
            WHERE id = (SELECT id
                        FROM CLIENTE
                        WHERE clave = %s)
        ''', (data['psw'], data['clave'] ) )
        mysql.connection.commit()
        
        return True
    except Exception as e:
        print(e)
        return 'Error en la base de datos'

    finally:
        cur.close()