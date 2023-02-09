from django.shortcuts import redirect
from rest_framework.decorators import api_view
from .models import Minyak, Poin
from .serializers import MinyakSerializers, PoinSerializer
from rest_framework.response import Response

#Riwayat semua inputan minyak
@api_view(["GET"])
def listMinyak(request):
    data = Minyak.objects.all()
    serializer = MinyakSerializers(data, many=True)
    return Response(serializer.data)

#Riwayat inputan minyak berdasarkan nama
@api_view(["GET"])
def detailMinyak(request,username):
    data = Minyak.objects.filter(user = username)
    serializer = MinyakSerializers(data, many=True)
    return Response(serializer.data)


#Input minyak + update poin
@api_view(["POST"])
def addMinyak(request):
    minyak = Minyak.objects.create(
        user = request.data["user"],
        volume = request.data["volume"]
    )
    try:
        Poin.objects.create(
            user = request.data["user"],
            poin = (int(minyak.volume) * 2)
        )
    except:
        poin = int(Poin.objects.get(user = request.data["user"]).poin + (minyak.volume * 2))
        updatePoin = Poin.objects.filter(user = request.data["user"])
        updatePoin.update(
            poin = poin
        )
    return redirect('/api/')

#Riwayat semua poin
@api_view(["GET"])
def poinView(request):
    data = Poin.objects.all()
    serializer = PoinSerializer(data, many=True)
    return Response(serializer.data)

#Riwayat semua poin berdasarkan nama
@api_view(["GET"])
def detailPoin(request, username):
    data = Poin.objects.filter(user = username)
    serializer = PoinSerializer(data, many=True)
    return Response(serializer.data)


# @api_view(["DELETE"])
# def deleteMinyak(request, delete_id):
#     minyak = Minyak.objects.get(id = delete_id)
#     poin = Poin.objects.get(user = minyak.user).poin
#     poin = poin - (int(minyak.volume) * 100)
#     Poin.objects.filter(user = minyak.user).update(
#         poin = poin
#     )
#     minyak = Minyak.objects.filter(id = delete_id).delete()
#     return redirect('/api/')