from djongo import models

class Mesin(models.Model):
    _id = models.ObjectIdField()
    nama = models.CharField(max_length=64)
    kapasitas = models.IntegerField()
    terisi = models.IntegerField()
    lokasi = models.TextField(max_length=128, unique=True)
    origin = models.TextField(max_length=128, unique=True)
    id_pengguna_aktif = models.CharField(max_length=128, blank=True, default='')

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.nama
    