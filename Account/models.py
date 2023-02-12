from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, models.Model):
    name = models.TextField(blank=True, max_length=32)
    email = models.EmailField(max_length=32, unique=True)
    phone = models.TextField(max_length=16, blank=True)
    alamat = models.TextField(max_length=128, blank=True)
    # poin = models.IntegerField(default=0)
    foto = models.TextField(max_length=128, blank=True)

    createdAt = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    updateAt = models.DateTimeField(
        verbose_name='date updated', auto_now_add=True)

    is_adminDesa = models.BooleanField(default=False)  # Admin Desa
    is_user = models.BooleanField(default=True)  # User
    is_superAdmin = models.BooleanField(default=False)  # Super Admin
    is_staff = models.BooleanField(default=False)  # Super Admin

    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # objects = AccountManager()

    # def __str__(self):
    #     return self.email

    # def has_perm(self, perm, obj=None):
    #     return self.is_adminDesa

    # def has_module_perms(self, app_label):
    #     return True
