from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
import jwt

class isAdmin(BasePermission):

   def has_permission(self, request, view):
        token = request.COOKIES.get('jwt')    
    
        if not token or token == '':
            raise AuthenticationFailed('Unauthenticated!')
            return False
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

            if payload['admin'] is False:
                raise AuthenticationFailed('Unauthenticated: Admin Only')
                return False
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
            return False
            
        request.account = payload
        return True
    
class isUser(BasePermission):

   def has_permission(self, request, view):
        token = request.COOKIES.get('jwt')    
    
        if not token or token == '':
            raise AuthenticationFailed('Unauthenticated!')
            return False
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

            if payload['admin'] is True:
                raise AuthenticationFailed('Unauthenticated: User Only')
                return False
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
            return False
            
        
        request.account = payload
        return True