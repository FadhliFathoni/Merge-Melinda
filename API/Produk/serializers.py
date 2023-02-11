from rest_framework import serializers
from .models import Produk, Kategori, Penukaran

class PenukaranSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Penukaran
        fields = '__all__'

class ProdukSerializers(serializers.ModelSerializer):
    penukaran = PenukaranSerializer(many=True)
    
    class Meta: 
        model = Produk
        fields = '__all__'

class KategoriSerializers(serializers.ModelSerializer):

    class Meta: 
        model = Kategori
        fields = '__all__'
        

    
        