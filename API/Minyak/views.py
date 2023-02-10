from django.shortcuts import redirect
from rest_framework.decorators import api_view
from .models import Minyak
from .serializers import MinyakSerializers, PoinSerializer
from rest_framework.response import Response
from Account.models import Account
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter

class MinyakPagination(PageNumberPagination):
    page_size = 5
    def get_page_size(self, request):
        return super().get_page_size(request)

class ListMinyak(ListAPIView):
    queryset = Minyak.objects.filter(status = "Terverifikasi")
    serializer_class = MinyakSerializers
    pagination_class = MinyakPagination
    filter_backends = [OrderingFilter,SearchFilter]
    search_fields = ("user","email")
    ordering = ["-created"]

@api_view(["POST"])
def addMinyak(request):
    try:
        user = Account.objects.get(name = request.data["user"])
        Minyak.objects.create(
            user = user.name,
            id_user = user.id,
            email = user.email,
            phone = user.phone,
        )
    except:
        return Response("Username tidak tersedia")

class ListPoin(ListAPIView):
    queryset = Minyak.objects.filter(status = "Terverifikasi")
    serializer_class = PoinSerializer
    pagination_class = MinyakPagination
    filter_backends = [OrderingFilter,SearchFilter]
    search_fields = ("user","email")
    ordering = ["-created"]

class Setoran(ListAPIView):
    queryset = Minyak.objects.filter(status = "Menunggu Verifikasi")
    serializer_class = MinyakSerializers
    pagination_class = MinyakPagination
    filter_backends = [OrderingFilter,SearchFilter]
    search_fields = ("user","email")
    ordering = ["-created"]

@api_view(["POST"])
def Verifikasi(request, id):
    data = Minyak.objects.filter(id = id)
    if "volume" in request.data:
        data.update(
            volume = request.data["volume"],
            poin = int(request.data["volume"] / 500),
            status = "Terverifikasi"
        )
        serializer = MinyakSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
    return Response(serializer.data)