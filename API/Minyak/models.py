from django.db import models

class Minyak(models.Model):
    user = models.CharField(max_length=50)
    id_user = models.CharField(max_length=128, null=True)
    # nama = models.CharField(max_length=32)
    email = models.EmailField(null=True)
    phone = models.TextField(max_length=16,null=True)
    volume = models.IntegerField(null=True)
    poin = models.IntegerField(null=True)
    status = models.CharField(max_length=50, default="Menunggu Verifikasi")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)