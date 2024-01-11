from flask import session

def verifyUser():
    user = [
        session.get('user_id', None),
        session.get('user_name', None)
    ]
    
    return user