from django.contrib import admin
from .models import CustomBaseUser, Otp, Token, Timestamp

# Register your models here.
admin.site.register(CustomBaseUser)
admin.site.register(Otp)
admin.site.register(Token)
# admin.site.register(Timestamp)

