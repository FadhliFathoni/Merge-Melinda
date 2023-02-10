from django.shortcuts import redirect
from rest_framework.decorators import api_view
from .models import Minyak
from .serializers import MinyakSerializers, PoinSerializer
from rest_framework.response import Response
from Account.models import Account
from rest_framework.generics import ListAPIView

class ListMinyak(ListAPIView):
    queryset = Minyak.objects.filter(status = "Terverifikasi")
    serializer_class = MinyakSerializers
    

@api_view(["POST"])
def addMinyak(request):
    try:
        user = Account.objects.get(name = request.data["user"])
        Minyak.objects.create(
            user = user.name,
            id_user = user.id,
            email = user.email,
            phone = user.phone,
            volume = request.data["volume"],
        )
    except:
        return Response("Username tidak tersedia")

class ListPoin(ListAPIView):
    queryset = Minyak.objects.filter(status = "Terverifikasi")
    serializer_class = PoinSerializer

class Setoran(ListAPIView):
    queryset = Minyak.objects.filter(status = "Menunggu Verifikasi")
    serializer_class = MinyakSerializers

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