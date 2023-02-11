from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from Account.models import Account
from django.contrib.auth import login, authenticate

@api_view(["GET","POST"])
def loginView(request):
    if request.method == "POST":
        email = request.data["email"]
        password = request.data["password"]
        data = Account.objects.get(email = email)
        akun = authenticate(email = email, password = password)
        if akun is not None:
            login(request, akun)
            return Response(data.id)
    return Response("Login")