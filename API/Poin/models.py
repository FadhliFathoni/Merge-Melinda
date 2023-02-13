from djongo import models

class Poin(models.Model):
    id_user = models.IntegerField()
    email = models.EmailField(max_length=50,unique=True)
    poin = models.IntegerField(default=0)