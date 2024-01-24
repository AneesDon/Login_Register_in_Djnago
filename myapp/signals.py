from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomBaseUser, Token, Otp
import random
from datetime import datetime, timedelta
import pytz


@receiver(post_save, sender=CustomBaseUser)

def user_created(sender, instance, created, **kwargs, ):
    if created:
        token = str(random.random()).split('.')[1]
        token_save = Token(token_data=token, user=instance)
        token_save.save()
        print("token generated")
        link = f"http://127.0.0.1:8000//acc_active_email/{token}"
        (send_mail(
            "Verify Your Mail",
            f"Click on this link to verify your mail {link}",
            settings.EMAIL_HOST_USER,
            [instance],
            fail_silently=False
        ))


@receiver(post_save, sender=Otp)
def otp_generated(sender, instance, created, **kwargs, ):

    if created:
        send_mail(
            "OTP For Forget Pasword",
            f"Your OPT:-   {instance.otp_data}",
            settings.EMAIL_HOST_USER,
            [instance.user],
            fail_silently=False
        )


