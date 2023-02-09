from .models import Minyak, Poin
from rest_framework import serializers

class MinyakSerializers(serializers.ModelSerializer):
    class Meta:
        model = Minyak
        fields = "__all__"

class PoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poin
        fields = "__all__"