from django.shortcuts import redirect
from rest_framework.decorators import api_view
from .models import Minyak
from .serializers import MinyakSerializers, PoinSerializer
from rest_framework.response import Response
from Account.models import User
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
import datetime

class MinyakPagination(PageNumberPagination):
    page_size = 5

    def get_page_size(self, request):
        if "limit" in request.GET:
            self.page_size = request.GET["limit"]
        return super().get_page_size(request)


class ListMinyak(ListAPIView):
    queryset = Minyak.objects.filter(status="Terverifikasi")
    serializer_class = MinyakSerializers
    pagination_class = MinyakPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ("user", "email")
    ordering = ["-created"]


@api_view(["POST"])
def addMinyak(request):
    try:
        user = User.objects.get(name=request.data["user"])
        try:
            Minyak.objects.create(
                user=user.name,
                id_user=user.id,
                email=user.email,
                phone=user.phone,
            )
            return Response("Berhasil")
        except:
            return Response("Gagal")
    except:
        return Response("Username tidak tersedia")

class ListPoin(ListAPIView):
    queryset = Minyak.objects.filter(status="Terverifikasi")
    serializer_class = PoinSerializer
    pagination_class = MinyakPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ("user", "email")
    ordering = ["-created"]


class Setoran(ListAPIView):
    queryset = Minyak.objects.filter(status="Menunggu Verifikasi")
    serializer_class = MinyakSerializers
    pagination_class = MinyakPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ("user", "email")
    ordering = ["-created"]


@api_view(["POST"])
def Verifikasi(request, id):
    data = Minyak.objects.filter(id=id)
    if "volume" in request.data:
        if int(request.data["volume"]) >= 500:
            data.update(
                volume = request.data["volume"],
                poin = int(request.data["volume"]) / 500,
                status = "Terverifikasi",
            )
            serializer = MinyakSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response("Berhasil")
        else:
            return Response("Volume kurang")
    return Response(serializer.data)
