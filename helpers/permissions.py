from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from functools import wraps
import jwt

def has_access(request, roles):
    token = request.COOKIES.get('jwt') or request.headers.get('jwt') 
    
    if not token or token == '':
        raise AuthenticationFailed('Unauthenticated: you need to login')
        return False
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
       
        if roles != "*" :       
            payloadRoles = []        
            
            for key in payload:
                if payload[key] == True: payloadRoles.append(key)
                    
            if len(list(set(payloadRoles) & set(roles))) == 0:
                raise AuthenticationFailed('Unauthenticated: you are not allowed')
                return False
        
    except (jwt.ExpiredSignatureError, KeyError):
        raise AuthenticationFailed('Unauthenticated: you need to login')
        return False
        
    request.account = payload
    return True
