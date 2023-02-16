from djongo import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, phone, name):
        if not email:
            raise ValueError("Users must have an email")

        user = self.model(email=self.normalize_email(
            email), phone=phone, name=name)

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        user = self.model(
            email=self.normalize_email(email),
        )
        user.is_adminDesa = True
        user.is_user = True
        user.is_superAdmin = True
        user.is_staff = True
        user.is_superuser = True

        # user.poin = None

        user.set_password(password)
        user.save(using=self.db)
        return user


# class Account(AbstractBaseUser):
#     name = models.TextField(blank=True, max_length=32,unique=True)
#     email = models.EmailField(verbose_name="email", max_length=32, unique=True)
#     phone = models.TextField(max_length=16)
#     alamat = models.TextField(max_length=128)
#     poin = models.IntegerField(default=0)
#     foto = models.TextField(max_length=128)
class User(AbstractUser, models.Model):
    _id = models.ObjectIdField()
    name = models.TextField(blank=True, max_length=32, unique=True)
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

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
