from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,PermissionsMixin
from .manager import CustomUserManager

# Create your models here.

class Timestamp(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)


class CustomBaseUser(AbstractBaseUser, PermissionsMixin, Timestamp):

    username = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"

    def __str__(self):
        return self.email


class Token(Timestamp):
    token_data = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(CustomBaseUser, on_delete=models.CASCADE, related_name='user')


class Otp(Timestamp):
    otp_data = models.IntegerField(null=False, default="100")
    user = models.OneToOneField(CustomBaseUser, on_delete=models.CASCADE)

    def __int__(self):
        return self.otp_data




