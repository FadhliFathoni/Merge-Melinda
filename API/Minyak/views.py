from django.shortcuts import redirect
from rest_framework.decorators import api_view
from .models import Minyak
from .serializers import MinyakSerializers
from rest_framework.response import Response
from Account.models import User
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
import datetime
from API.Poin.models import Poin
from API.Poin.serializers import PoinSerializer
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from calendar import monthrange
from bson.objectid import ObjectId

import sys

class MinyakPagination(PageNumberPagination):
    page_size = 5

    def get_page_size(self, request):
        if "limit" in request.GET:
            self.page_size = request.GET["limit"]
        return super().get_page_size(request)


class ListMinyak(ListAPIView):
    serializer_class = MinyakSerializers
    pagination_class = MinyakPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ("user", "email")
    ordering = ["-updated"]

    def get_queryset(self):
        now = datetime.now().date()
        queryset = Minyak.objects.filter(status="Terverifikasi")
        
        if "start" in self.request.GET and "end" in self.request.GET:
                start = self.request.GET["start"]
                end = self.request.GET["end"]
                queryset = Minyak.objects.filter(status="Terverifikasi", created__range = [start,end])
                total = 0
                for x in queryset:
                    total = total + x.volume
                print(total)
        # if "date" in self.request.GET:
        #     date = self.request.GET["date"]
        #     if date == "today":
        #         print("Today")
        #         queryset = Minyak.objects.filter(status="Terverifikasi",created__icontains = now)
        #     elif date == "yesterday":
        #         queryset = Minyak.objects.filter(status = "Terverifikasi",created__icontains = now-relativedelta(days=1))
        return queryset

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
            print(sys.exc_info())
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
    userData = Minyak.objects.get(id = id)
    email = User.objects.get(id = userData.id_user)
    
    if "volume" in request.data:
        if int(request.data["volume"]) >= 500:
            poin = int(request.data["volume"]) / 500
            volume = int(request.data["volume"])

            data.update(
                volume = volume,
                poin = poin,
                status = "Terverifikasi",
                updated = now()
            )
            try:
                Poin.objects.create(
                id_user = userData.id,
                nama = userData.user,
                email = email,
                poin = poin,
                volume = volume
                )
            except:
                poin = int(Poin.objects.get(email = email).poin + poin)
                volume = int(Poin.objects.get(email = email).volume + volume)
                updatePoin = Poin.objects.filter(email = email)
                updatePoin.update(
                    poin = poin,
                    volume = volume
                )
                pserializer = PoinSerializer(data = updatePoin)
                if pserializer.is_valid():
                    pserializer.save()
            serializer = MinyakSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response("Berhasil")
        else:
            return Response("Volume kurang")
    return Response("Verifikasi")
