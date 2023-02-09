from djongo import models
# from django.db import models as modelsDJA
# from djongo.models import indexes

class Kategori(models.Model):
    _id = models.ObjectIdField()
    nama = models.CharField(max_length=64)

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.nama



class Penukaran(models.Model):
    _id = models.ObjectIdField()
    id_pengguna = models.CharField(max_length=128)
    kode = models.CharField(max_length=16, default='xxx') # baru
    jumlah = models.IntegerField()
    tanggal = models.DateField()
    selesai = models.BooleanField(default=False) # barau

    # class Meta:
    #     abstract = True
    
class Produk(models.Model):
    _id = models.ObjectIdField()
    nama = models.CharField(max_length=64)
    stok = models.IntegerField()
    keterangan = models.CharField(max_length=128)
    id_mesin = models.CharField(max_length=128)
    gambar = models.CharField(max_length=128)
    harga = models.IntegerField()
    kategori = models.CharField(max_length=200, default="")
    penukaran = models.ArrayField(
        model_container = Penukaran,
        default=[]
    )
    
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    # class Meta: 
    #     indexes = [
    #         indexes.Index. (fields=['nama', 'keterangan'])
    #     ]
    def __str__(self):
        return self.nama
