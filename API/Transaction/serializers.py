from .models import Transaksi
from rest_framework import serializers


class TransaksiSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transaksi
        fields = "__all__"
