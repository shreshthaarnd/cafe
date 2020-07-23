from django.shortcuts import render, redirect
from django.views.decorators.csrf import *
from app.models import *
from django.core.paginator import *
from django.core.mail import EmailMessage
from django.http import HttpResponse
import uuid
#from app.myutil import *
import csv
from datetime import date
from django.conf import settings
# Create your views here.
def index(request):
	return render(request,'index.html',{})
def about(request):
	return render(request,'about.html',{})
def chefs(request):
	return render(request,'chefs.html',{})
def contact(request):
	return render(request,'contact.html',{})
def elements(request):
	return render(request,'elements.html',{})
def foodmenu(request):
	return render(request,'food_menu.html',{})
def singleblog(request):
	return render(request,'single-blog.html',{})
def adminlogin(request):
	return render(request,'adminpages/login.html',{})
def adminlist(request):
	return render(request,'adminpages/agentlist.html',{})
def adminaddcategory(request):
	return render(request,'adminpages/addcategory.html',{})
@csrf_exempt
def adminlogincheck(request):
	if request.method=='POST':
		email=request.POST.get('email')
		password=request.POST.get('password')
		if email == 'admin@cafeliant.com' and password == '1234':
			request.session['admin'] = email
			return redirect('/adminindex/')
		else:
			return HttpResponse("<script>alert('Incorrect Credentials'); window.location.replace('/adminlogin/')</script>")
	else:
		return redirect('/index/')
def adminindex(request):
	try:
		admin=request.session['admin']
		return render(request,'adminpages/index.html',{})
	except:
		return redirect('/index/')
def adminlogout(request):
	try:
		del request.session['admin']
		return redirect('/adminlogin/')
	except:
		return redirect('/index/')