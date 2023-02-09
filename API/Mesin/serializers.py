from rest_framework import serializers
from .models import Mesin

class MesinSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Mesin
        fields = '__all__'
