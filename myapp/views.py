from django.shortcuts import render,redirect
from .models import CustomBaseUser, Token, Otp
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import random
from datetime import datetime, timedelta
import pytz
from .decorators import buyer_required, seller_required
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def register(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        con_pass = request.POST.get('conpass')
        radio = request.POST.get('user_type')
        is_buyer = False
        is_seller = False
        if radio == "buyer":
            is_buyer = True
        if radio == "seller":
            is_seller = True

        if username and email and password and con_pass and radio:

            if password != con_pass:
                return render(request, "register.html", {"error": "Password & Confirm Password Not Matching"})

            user = CustomBaseUser.objects.create_user(email=email, password=password, username=username,
                                                      is_buyer=is_buyer, is_seller=is_seller)
            user.save()

            return HttpResponse("Mail Has Been Send To Your Mail ID, Please Check Your Inbox")

    else:
        return render(request,"register.html")


def activate(request, token):

    try:
        tokenObj = Token.objects.get(token_data=token)
        dtStr = datetime.strptime(str(tokenObj.created_at), '%Y-%m-%d %H:%M:%S.%f%z')

        afterTwo = dtStr + timedelta(minutes=2)
        afterTwoStr = afterTwo.strftime('%Y-%m-%d %H:%M:%S.%f%z')

        objTimeStr = datetime.strptime(afterTwoStr, '%Y-%m-%d %H:%M:%S.%f%z')

        current_datetime = datetime.now(pytz.utc)

        if current_datetime > objTimeStr:
            tokenObj.delete()
        else:
            print(tokenObj.user)
            user = tokenObj.user
            user.is_active = True
            user.save()
            tokenObj.delete()
            print(tokenObj.user.is_active)

        return HttpResponse("Email verified, Now You can login")
    except Exception as e:
        return HttpResponse("Token expi red")


def login(request):

    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        is_active = CustomBaseUser.objects.get(email=email).is_active

        if is_active:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)
                request.session['user'] = user.id
                user_type = CustomBaseUser.objects.get(email=user)
                if user_type.is_buyer:
                    request.session['type'] = 'buyer'
                    return redirect('buyer')
                else:
                    request.session['type'] = 'seller'
                    return redirect('seller')

            else:
                return render(request,"login.html",{"error": "incorrect ID or Password"})
        else:
            return render(request,"login.html",{"error": "Please Active Your account, Check your mail"})

    else:
        return render(request, "login.html")


@login_required
@buyer_required
def buyer(request):

        userid = request.session['user']
        user = CustomBaseUser.objects.get(id=userid)
        msg = "You are a buyer"
        return render(request, "buyer.html", {"msg": msg, "user": user})


@login_required
@seller_required
def seller(request):
    msg = "You are a seller"
    return render(request, "seller.html", {"msg": msg})


@login_required
def change_password(request, id):
    if request.method == "POST":
        cur_password = request.POST.get("password")
        new_password = request.POST.get("new_password")
        con_password = request.POST.get("con_password")

        if new_password == con_password:
            valid_user = CustomBaseUser.objects.get(id=id)
            if valid_user.check_password(cur_password):
                valid_user.set_password(new_password)
                valid_user.save()
                return render(request,"change_password.html",{"msg": "Password updated successfully"})
            else:
                return render(request, "change_password.html", {"msg": "Wrong current password"})

        else:
            return render(request, "change_password.html", {"msg": "Password and confirm passwords are not matching"})

    else:
        return render(request,"change_password.html")


def logout_function(request):

    logout(request)
    return redirect('login')


def find_account(request):

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user_obj = CustomBaseUser.objects.get(email=email)
            print(user_obj)
            if user_obj:
                otp = str(random.random()).split('.')[1][0:6]
                otp_obj = Otp(otp_data=otp, user=user_obj)
                otp_obj.save()
                request.session['otp'] = user_obj.id

                return redirect('submit_otp')
            else:
                return render(request,"findaccount.html", {"msg": "Account not found"})
        except CustomBaseUser.DoesNotExist:
            return render(request,"findaccount.html", {"msg": "Account not found"})

    return render(request,"findaccount.html")


def otp_verify(request):

    if request.method == "POST":
        otp_box = request.POST.get("otp")
        user_otp = request.session['otp']

        try:
            user_obj = CustomBaseUser.objects.get(id=user_otp)
            otp_obj = Otp.objects.get(user=user_obj)
            dtStr = datetime.strptime(str(otp_obj.created_at), '%Y-%m-%d %H:%M:%S.%f%z')

            afterTwo = dtStr + timedelta(minutes=2)
            afterTwoStr = afterTwo.strftime('%Y-%m-%d %H:%M:%S.%f%z')

            objTimeStr = datetime.strptime(afterTwoStr, '%Y-%m-%d %H:%M:%S.%f%z')

            current_datetime = datetime.now(pytz.utc)

            if current_datetime > objTimeStr:
                otp_obj.delete()
                return HttpResponse("OTP expired")
            else:
                if int(otp_obj.otp_data) == int(otp_box):
                    return redirect('new_password')
                else:
                    return render(request, "submit_otp.html", {"error": "Wrong Otp"})
        except ObjectDoesNotExist as e:
            HttpResponse(e)
    else:
        return render(request,"submit_otp.html")


def new_password(request):
    if request.method == "POST":
        user_otp = request.session['otp']
        password = request.POST.get("password")
        con_password = request.POST.get("conpassword")

        if password == con_password:
            try:
                user_obj = CustomBaseUser.objects.get(id=user_otp)
                user_obj.password = password
                user_obj.save()
                otp_obj = Otp.objects.get(user=user_obj)
                otp_obj.delete()
                return render(request, "new_password.html",{"msg": "Password updated successfully"})
            except ObjectDoesNotExist as e:
                HttpResponse(e)
        else:
            return render(request, "new_password.html",{"msg": "Password and confirm password not matching"})

    else:
        return render(request, "new_password.html")





