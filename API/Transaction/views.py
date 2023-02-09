from rest_framework.decorators import api_view
from .models import Transaksi
from .serializers import TransaksiSerializers
from rest_framework.response import Response
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now


# Semua Transaksi
@api_view(["GET"])
def semuaTransaksi(request):
    data = Transaksi.objects.all()
    serializer = TransaksiSerializers(data, many=True)
    return Response(serializer.data)


# Menambah Transaksi
@api_view(["POST"])
def addTransaksi(request):
    transaksi = Transaksi.objects.create(
        id_pengguna=request.data["id_pengguna"],
        id_mesin=request.data["id_mesin"],
        volume=request.data["volume"],
        poin=request.data["poin"],
        jenis=request.data["jenis"],
    )
    transaksi.save()


# Filter Transaksi (Hari ini)
@api_view(["GET"])
def filterSekarang(self):
    now = datetime.now().date()
    data = Transaksi.objects.filter(waktuTransaksi=now)
    serializer = TransaksiSerializers(data, many=True)
    return Response(serializer.data)


# Filter Transaksi (Kemarin)
@api_view(["GET"])
def filterHari(self):
    data = Transaksi.objects.filter(
        waktuTransaksi=now().date()-relativedelta(days=1))
    serializer = TransaksiSerializers(data, many=True)
    return Response(serializer.data)


# Filter Transaksi (Sebulan Terakhir)
@api_view(["GET"])
def filterBulan(self):
    data = Transaksi.objects.filter(
        waktuTransaksi=now().date()-relativedelta(months=1))
    serializer = TransaksiSerializers(data, many=True)
    return Response(serializer.data)


# Filter Transaksi (1 Tahun Terakhir)
@api_view(["GET"])
def filterTahun(self):
    data = Transaksi.objects.filter(
        waktuTransaksi=now().date()-relativedelta(years=1))
    serializer = TransaksiSerializers(data, many=True)
    return Response(serializer.data)
