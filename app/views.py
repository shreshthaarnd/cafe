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
def adminaddmenuitem(request):
	try:
		admin=request.session['admin']
		return render(request,'adminpages/addmenuitem.html',{})
	except:
		return redirect('/index/')
@csrf_exempt
def adminsavemenuitem(request):
	if request.method=='POST':
		name=request.POST.get('name')
		category=request.POST.get('category')
		price=request.POST.get('price')
		m="M00"
		x=1
		mid=m+str(x)
		while MenuData.objects.filter(Item_ID=mid).exists():
			x=x+1
			mid=m+str(x)
		x=int(x)
		obj=MenuData(
			Item_ID=mid,
			Item_Category=category,
			Item_Name=name,
			Item_Price=price
			)
		obj.save()
		dic={'msg':'Item Saved'}
		return render(request,'adminpages/addmenuitem.html',dic)
	else:
		return redirect('/index/')
def admineditmenuitem(request):
	try:
		admin=request.session['admin']
		name=request.GET.get('name')
		price=request.GET.get('price')
		itemid=request.GET.get('Id')
		obj=MenuData.objects.filter(Item_ID=itemid)
		obj.update(Item_Name=name, Item_Price=price)
		return redirect('/adminmenulist/')
	except:
		return redirect('/index/')

def admindeletemenuitem(request):
	try:
		admin=request.session['admin']
		itemid=request.GET.get('Id')
		obj=MenuData.objects.filter(Item_ID=itemid).delete()
		return redirect('/adminmenulist/')
	except:
		return redirect('/index/')

def adminmenulist(request):
	try:
		admin=request.session['admin']
		dic={'data':MenuData.objects.all()}
		return render(request,'adminpages/menulist.html',dic)
	except:
		return redirect('/index/')
def adminaddmenucategory(request):
	try:
		admin=request.session['admin']
		dic={'data':MenuCategoryData.objects.all()}
		return render(request,'adminpages/addmenucategory.html',dic)
	except:
		return redirect('/index/')

@csrf_exempt
def adminsavemenucategory(request):
	if request.method=='POST':
		name=request.POST.get('name')
		m="C00"
		x=1
		mid=m+str(x)
		while MenuCategoryData.objects.filter(Category_ID=mid).exists():
			x=x+1
			mid=m+str(x)
		x=int(x)
		obj=MenuCategoryData(
			Category_ID=mid,
			Category_Name=name
		)
		if MenuCategoryData.objects.filter(Category_Name=name).exists():
			dic={'data':MenuCategoryData.objects.all(),
				'msg':'Category Already Exists'}
			return render(request,'adminpages/addmenucategory.html',dic)
		else:
			obj.save()
			dic={'data':MenuCategoryData.objects.all(),
				'msg':'Saved!'}
			return render(request,'adminpages/addmenucategory.html',dic)
	else:
		return redirect('/index/')

def admineditmenucategory(request):
	try:
		admin=request.session['admin']
		name=request.GET.get('name')
		itemid=request.GET.get('Id')
		obj=MenuCategoryData.objects.filter(Category_ID=itemid)
		obj.update(Category_Name=name)
		return redirect('/adminaddmenucategory/')
	except:
		return redirect('/index/')

def admindeletemenucategory(request):
	try:
		admin=request.session['admin']
		itemid=request.GET.get('Id')
		obj=MenuCategoryData.objects.filter(Category_ID=itemid).delete()
		return redirect('/adminaddmenucategory/')
	except:
		return redirect('/index/')
def adminadddiscountcoupon(request):
	return render(request,'adminpages/adddiscountcoupon.html',{})
def admindiscountcouponlist(request):
	return render(request,'adminpages/discountcouponlist.html',{})
def adminongoingorder(request):
	return render(request,'adminpages/ongoingorder.html',{})