from django.shortcuts import redirect
from rest_framework.generics import ListAPIView, DestroyAPIView, GenericAPIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import InvalidPage
from Account.models import User
from API.Minyak.models import Minyak
from API.Minyak.serializers import MinyakSerializers
from API.Poin.models import Poin
from API.Poin.serializers import PoinSerializer
from rest_framework.mixins import DestroyModelMixin


class UserPagination(PageNumberPagination):
    page_size = 5

    def get_page_size(self, request):
        if "limit" in request.GET:
            self.page_size = request.GET["limit"]
        return super().get_page_size(request)


class ListUser(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ("name", "email")
    pagination_class = UserPagination
    ordering = ["-createdAt"]

# @api_view(["DELETE"])
# def deleteUser(request,pk):
#     try:
#         User.objects.filter(id = pk).delete()
#         Minyak.objects.filter(id_user = pk).delete()
#         Poin.objects.filter(id_user = pk).delete()
#     except:
#         return Response("Delete Invalid")


class deleteUser(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class destroyUser(GenericAPIView,DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        print(kwargs["pk"])
        User.objects.filter(id = kwargs["pk"]).delete()
        Minyak.objects.filter(id_user = kwargs["pk"]).delete()
        Poin.objects.filter(id_user = kwargs["pk"]).delete()
        return super().destroy(request, *args, **kwargs)