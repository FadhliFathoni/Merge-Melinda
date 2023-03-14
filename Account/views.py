from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer
from .models import User
import jwt
import datetime
from jwt import decode
from bson.objectid import ObjectId

import sys

from helpers.permissions import has_access

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email__exact=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': str(user._id),
            'is_superAdmin': user.is_superAdmin,
            'is_staff': user.is_staff,
            'is_user': user.is_user,
            'is_adminDesa': user.is_adminDesa, 
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    
    def get(self, request):
        if not has_access(request, "*"): raise AuthenticationFailed('Unauthenticated: you are not allowed')
        
        user = User.objects.filter(_id=ObjectId(request.account['id'])).first()
        serializer = UserSerializer(user)
        
        return Response(serializer.data)



class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
