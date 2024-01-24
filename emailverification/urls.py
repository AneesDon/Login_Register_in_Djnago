"""emailverification URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name="register"),
    path('acc_active_email/<str:token>/', views.activate,
         name='activate'),
    path('login/', views.login, name="login"),
    path('buyer/', views.buyer, name="buyer"),
    path('seller/', views.seller, name="seller"),
    path('changepassword/<int:id>/', views.change_password, name="changepassword"),
    path('findaccount/', views.find_account, name="findaccount"),
    path('logout/', views.logout_function, name="logout"),
    path('submit_otp/', views.otp_verify, name="submit_otp"),
    path('new_password/', views.new_password, name="new_password"),

]
