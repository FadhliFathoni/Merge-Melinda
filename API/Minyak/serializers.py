from .models import Minyak
from rest_framework import serializers

class MinyakSerializers(serializers.ModelSerializer):
    class Meta:
        model = Minyak
        fields = "__all__"

class PoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Minyak
        fields = ["id","user","id_user","email","phone", "volume","poin","status"]