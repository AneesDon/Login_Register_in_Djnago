from functools import wraps
from django.shortcuts import render, redirect
from .models import CustomBaseUser
from django.http import HttpResponseForbidden,HttpResponse


def buyer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user' in request.session:
            user_id = request.session['user']
            user_obj = CustomBaseUser.objects.get(id=user_id)
            if user_obj.is_seller:
                return render(request,'seller.html',{'error': "you are a seller you can't access this page"})
                # HttpResponse("You are not a buyer ")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def seller_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user' in request.session:
            user_id = request.session['user']
            user_obj = CustomBaseUser.objects.get(id=user_id)
            if user_obj.is_buyer:
                return render(request,'buyer.html',{'error': "you are a buyer you can't access this page"})
        return view_func(request, *args, **kwargs)
    return _wrapped_view



