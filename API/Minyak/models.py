from django.db import models

class Minyak(models.Model):
    user = models.CharField(max_length=50)
    volume = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Poin(models.Model):
    user = models.CharField(max_length=50,unique=True)
    poin = models.IntegerField(default=0)