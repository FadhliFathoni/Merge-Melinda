from django.shortcuts import redirect
from rest_framework.generics import ListAPIView, DestroyAPIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import InvalidPage
from Account.models import User


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
# def deleteUser(request,delete_id):
#     User.objects.filter(id = delete_id).first().delete()


class deleteUser(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
