from djongo import models

class Poin(models.Model):
    _id = models.ObjectIdField()
    id_user = models.CharField(max_length=128)
    nama = models.CharField(max_length=64)
    email = models.EmailField(max_length=50,unique=True)
    poin = models.IntegerField(default=0)
    volume = models.IntegerField(default=0)