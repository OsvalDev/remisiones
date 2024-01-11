from flask import session

def verifyUser():
    user = [
        session.get('user_id', None),
        session.get('user_name', None),
        session.get('privilegiesList', None)
    ]
    
    return user