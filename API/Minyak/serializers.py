from .models import Minyak
from rest_framework import serializers

class MinyakSerializers(serializers.ModelSerializer):
    class Meta:
        model = Minyak
        fields = "__all__"