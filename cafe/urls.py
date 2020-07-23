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
    path('index/',index),
    path('about/',about),
    path('chefs/',chefs),
    path('contact/',contact),
    path('elements/',elements),
    path('foodmenu/',foodmenu),
    path('singleblog/',singleblog),
    path('adminlogin/',adminlogin),
    path('adminlogincheck/',adminlogincheck),
    path('adminlogout/',adminlogout),
    path('adminindex/',adminindex),
    path('adminlist/',adminlist),
    path('adminaddcategory/',adminaddcategory),
    path('adminaddmenuitem/',adminaddmenuitem),
    path('adminsavemenuitem/',adminsavemenuitem),
    path('admineditmenuitem/',admineditmenuitem),
    path('admindeletemenuitem/',admindeletemenuitem),
    path('adminmenulist/',adminmenulist),
]