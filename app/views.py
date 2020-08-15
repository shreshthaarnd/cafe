from django.shortcuts import render, redirect
from django.views.decorators.csrf import *
from app.models import *
from django.core.paginator import *
from django.core.mail import EmailMessage
from django.http import HttpResponse
import uuid
#from app.myutil import *
import csv
from django.conf import settings
# Create your views here.
def index(request):
	return render(request,'index.html',{})
def adminlogin(request):
	return render(request,'adminpages/login.html',{})
def adminlist(request):
	return render(request,'adminpages/list.html',{})
def about(request):
	return render(request,'about.html',{})
def blog(request):
	return render(request,'blog.html',{})
def contact(request):
	return render(request,'contact.html',{})
def elements(request):
	return render(request,'elements.html',{})
def menu(request):
	return render(request,'menu.html',{})
def singleblog(request):
	return render(request,'single-blog.html',{})
def adminorderhistory(request):
	return render(request,'adminpages/orderhistory.html',{})
def adminproceedtopay(request):
	return render(request,'adminpages/proceedtopay.html',{})
def admincustomerlist(request):
	return render(request,'adminpages/customerlist.html',{})
def menucategory(request):
	return render(request,'menucategory.html',{})
def adminblockedcustomer(request):
	return render(request,'adminpages/blockedcustomer.html',{})
def adminchangemanager(request):
	return render(request,'adminpages/changemanager.html',{})
def admindeactivemenu(request):
	return render(request,'adminpages/deactivemenu.html',{})
def admindiscountcouponhistory(request):
	return render(request,'adminpages/discountcouponhistory.html',{})
def adminpaymenthistory(request):
	return render(request,'adminpages/paymenthistory.html',{})
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
		dic={'data':MenuCategoryData.objects.all()}
		return render(request,'adminpages/addmenuitem.html',dic)
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
		dic={'data':MenuCategoryData.objects.all(),
			'msg':'Item Saved'}
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
	try:
		admin=request.session['admin']
		dic={'ordermenudata':OrderMenuData.objects.all(),
			'items':MenuData.objects.all(),
			'orderdata':OrderData.objects.all(),
			'category':MenuCategoryData.objects.all()}
		return render(request,'adminpages/ongoingorder.html',dic)
	except:
		return redirect('/index/')
@csrf_exempt
def admincreateorder(request):
	if request.method=='POST':
		items=request.POST.getlist('items')
		o="O00"
		x=1
		oid=o+str(x)
		while OrderData.objects.filter(Order_ID=oid).exists():
			x=x+1
			oid=o+str(x)
		x=int(x)
		obj=OrderData(Order_ID=oid).save()
		for x in items:
			obj=OrderMenuData(Item_ID=x,Order_ID=oid).save()
		dic={'items':MenuData.objects.all(),
			 'category':MenuCategoryData.objects.all(),
			 'orderdata':OrderData.objects.all(),
			 'ordermenudata':OrderMenuData.objects.all(),
			'msg':'Order Created Successfully and Added to the Below List'}
		return render(request,'adminpages/ongoingorder.html',dic)
	else:
		return redirect('/index/')
@csrf_exempt
def adminsaveordermenu(request):
	if request.method == 'POST':
		orderid=request.POST.get('orderid')
		for x in OrderMenuData.objects.filter(Order_ID=orderid):
			obj=OrderMenuData.objects.filter(Order_ID=orderid, Item_ID=x.Item_ID)
			quantity=request.POST.get(x.Item_ID+x.Order_ID)
			if quantity == '0':
				obj.delete()
			else:
				obj.update(Quantity=quantity)
		return redirect('/adminongoingorder/')
	else:
		return redirect('/index/')
@csrf_exempt
def adminaddmoreitemstoorder(request):
	if request.method=='POST':
		items=request.POST.getlist('items')
		oid=request.POST.get('orderid')
		for x in items:
			if OrderMenuData.objects.filter(Item_ID=x,Order_ID=oid).exists():
				quantity=0
				for x in OrderMenuData.objects.filter(Item_ID=x,Order_ID=oid):
					quantity=int(x.Quantity)
				OrderMenuData.objects.filter(Item_ID=x,Order_ID=oid).update(Quantity=str(quantity+1))
			else:
				obj=OrderMenuData(Item_ID=x,Order_ID=oid).save()
		return redirect('/adminongoingorder/')
	else:
		return redirect('/index/')

def admincancelorder(request):
	if request.method=='GET':
		oid=request.GET.get('orderid')
		OrderData.objects.filter(Order_ID=oid).delete()
		OrderMenuData.objects.filter(Order_ID=oid).delete()
		return redirect('/adminongoingorder/')
	else:
		return redirect('/index/')

def adminsearchcustomer(request):
	try:
		admin=request.session['admin']
		oid=request.GET.get('orderid')
		request.session['orderid'] = oid
		total=0
		for x in OrderMenuData.objects.filter(Order_ID=oid):
			for y in MenuData.objects.filter(Item_ID=x.Item_ID):
				price=int(y.Item_Price)
				total=total+(price*int(x.Quantity))
		dic={'customers':CustomerData.objects.all(),
			'orderid':oid,
			'totalamount':str(total)}
		return render(request,'adminpages/searchcustomer.html',dic)
	except:
		return redirect('/index/')

def admincustomersearchresult(request):
#	try:
		admin=request.session['admin']
		cmobile=request.GET.get('cmobile')
		result=CustomerData.objects.filter(Mobile=cmobile)
		oid=request.session['orderid']
		total=0
		for x in OrderMenuData.objects.filter(Order_ID=oid):
			for y in MenuData.objects.filter(Item_ID=x.Item_ID):
				price=int(y.Item_Price)
				total=total+(price*int(x.Quantity))
		dic={'customers':CustomerData.objects.all(),
			'result':result,
			'orderid':oid,
			'totalamount':str(total)}
		return render(request,'adminpages/searchcustomer.html',dic)
#	except:
#		return redirect('/index/')
def adminpaybycard(request):
	return render(request,'adminpages/paybycard.html',{})
def adminpaybycash(request):
	return render(request,'adminpages/paybycash.html',{})
def adminpaybyqr(request):
	return render(request,'adminpages/paybyqr.html',{})
def adminbilinginvoice(request):
	return render(request,'adminpages/bilinginvoice.html',{})
def admintax(request):
	return render(request,'adminpages/tax.html',{})