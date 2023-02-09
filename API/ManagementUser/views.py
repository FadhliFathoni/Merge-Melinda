from django.shortcuts import redirect
from rest_framework.generics import ListAPIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response

class UserPagination(PageNumberPagination):
    page_size = 10

class ListUser(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ("username","email","date__joined")
    pagination_class = UserPagination

@api_view(["DELETE"])
def deleteUser(request,delete_id):
    User.objects.filter(id = delete_id).delete()
    return redirect("/user/")