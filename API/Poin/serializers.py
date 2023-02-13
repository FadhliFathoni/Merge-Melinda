from .models import Poin
from rest_framework import serializers

class PoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poin
        fields = "__all__"