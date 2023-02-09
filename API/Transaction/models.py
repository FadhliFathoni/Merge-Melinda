from django.db import models
from datetime import datetime
from django.utils.timezone import now

# Create your models here.


class Transaksi(models.Model):
    id_pengguna = models.TextField(default="123")
    id_mesin = models.TextField(default="123")
    volume = models.IntegerField(blank=True)
    poin = models.IntegerField(blank=True)
    jenis = models.TextField(blank=True)
    waktuTransaksi = models.TextField(default=now().date())
    cretedAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
