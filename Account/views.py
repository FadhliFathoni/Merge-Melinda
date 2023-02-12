from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt
import datetime


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
            'id': user.id,
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
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
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

# from django.shortcuts import render, redirect
# from django.contrib.auth.models import auth
# from django.contrib import messages

# from django.contrib.auth import get_user_model

# Account = get_user_model()

# # Create your views here.


# def home(request):
#     return render(request, "home.html")


# def register(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         phone = request.POST['phone']
#         email = request.POST['email']
#         password = request.POST['password']
#         if Account.objects.filter(email=email).exists():
#             messages.info(request, 'email is already exist')
#             return redirect(register)
#         else:
#             user = Account.objects.create_user(
#                 password=password, email=email, phone=phone, name=name)
#             user.set_password(password)
#             user.save()
#             return redirect('login_user')
#     else:
#         print("this is not post method")
#         return render(request, "register.html")


# def login_user(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']

#         user = auth.authenticate(email=email, password=password)

#         if user is not None:
#             auth.login(request, user)
#             return redirect('home')
#         else:
#             messages.info(request, 'Invalid email or password')
#             return redirect('login_user')

#     else:
#         return render(request, "login.html")


# def logout_user(request):
#     auth.logout(request)
#     return redirect('home')
