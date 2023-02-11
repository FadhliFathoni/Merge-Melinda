from djongo import models
# from django.db import models as modelsDJA
# from djongo.models import indexes

class Kategori(models.Model):
    _id = models.ObjectIdField()
    nama = models.CharField(max_length=64)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama


def uploadTo(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Produk(models.Model):
    _id = models.ObjectIdField()
    nama = models.CharField(max_length=64)
    stok = models.IntegerField()
    keterangan = models.CharField(max_length=128)
    id_mesin = models.CharField(max_length=128)
    gambar = models.ImageField(upload_to=uploadTo, blank=True, null=True)
    harga = models.IntegerField()
    kategori = models.CharField(max_length=200, default="")
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

class Penukaran(models.Model):
    _id = models.ObjectIdField()
    nama = models.CharField(max_length=128)
    kode = models.CharField(max_length=16, default='xxx') # baru
    email = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    produk = models.CharField(max_length=128)
    jumlah = models.IntegerField()
    tanggal = models.DateTimeField()
    selesai = models.BooleanField(default=False) # barau

    def __str__(self):
        return self.nama
    # class Meta:
    #     abstract = True
