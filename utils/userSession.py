from flask import session

def verifyUser():
    user = [
        session.get('user_id', None),
        session.get('user_name', None),
        session.get('privilegiesList', None)
    ]
    
    return user

def verifyCostumer():
    user = [
        session.get('costumer_id', None),
        session.get('costumer_name', None)
    ]
    
    return user