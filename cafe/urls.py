"""cafe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminlogin/',adminlogin),
    path('adminlogincheck/',adminlogincheck),
    path('adminlogout/',adminlogout),
    path('adminindex/',adminindex),
    path('adminaddmenuitem/',adminaddmenuitem),
    path('adminsavemenuitem/',adminsavemenuitem),
    path('admineditmenuitem/',admineditmenuitem),
    path('admindeletemenuitem/',admindeletemenuitem),
    path('adminmenulist/',adminmenulist),
    path('adminaddmenucategory/',adminaddmenucategory),
    path('adminsavemenucategory/',adminsavemenucategory),
    path('admineditmenucategory/',admineditmenucategory),
    path('admindeletemenucategory/',admindeletemenucategory),
    path('adminadddiscountcoupon/',adminadddiscountcoupon),
    path('admindiscountcouponlist/',admindiscountcouponlist),
    path('adminongoingorder/',adminongoingorder),
    path('index/',index),
    path('about/',about),
    path('blog/',blog),
    path('contact/',contact),
    path('elements/',elements),
    path('menu/',menu),
    path('singleblog/',singleblog),
    path('admincreateorder/',admincreateorder),
    path('adminorderhistory/',adminorderhistory),
    path('adminproceedtopay/',adminproceedtopay),
    path('admincustomerlist/',admincustomerlist),
    path('adminsaveordermenu/',adminsaveordermenu),
    path('menucategory/',menucategory),
    path('adminblockedcustomer/',adminblockedcustomer),
    path('adminchangemanager/',adminchangemanager),
    path('admindeactivemenu/',admindeactivemenu),
    path('admindiscountcouponhistory/',admindiscountcouponhistory),
    path('adminpaymenthistory/',adminpaymenthistory),
    path('adminaddmoreitemstoorder/',adminaddmoreitemstoorder),
    path('admincancelorder/',admincancelorder),
    path('adminsearchcustomer/',adminsearchcustomer),
    path('admincustomersearchresult/',admincustomersearchresult),
]
