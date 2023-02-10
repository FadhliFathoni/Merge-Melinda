from django.shortcuts import redirect
from rest_framework.generics import ListAPIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Account.models import Account

class UserPagination(PageNumberPagination):
    page_size = 5
    def get_page_size(self, request):
        if "limit" in request.GET:
            self.page_size = request.GET["limit"]
        return super().get_page_size(request)


class ListUser(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = UserSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ("username","email","date__joined")
    pagination_class = UserPagination

        

@api_view(["DELETE"])
def deleteUser(request,delete_id):
    Account.objects.filter(id = delete_id).first().delete()
    return redirect("/user/")