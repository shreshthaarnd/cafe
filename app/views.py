from django.shortcuts import render, redirect
from django.views.decorators.csrf import *
from app.models import *
from django.core.paginator import *
from django.core.mail import EmailMessage
from django.http import HttpResponse
import uuid
from app.myutil import *
import csv
from django.conf import settings
import datetime
from app.mailutil import *
from app.sms import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, filters
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
import requests
import json
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
	display = []
	for x in MenuCategoryData.objects.all():
		if MenuData.objects.filter(Status='Active', Item_Category=x.Category_ID).exists():
			display.append(x.Category_ID)
	dic={'menu':MenuData.objects.filter(Status='Active'),
		'category':MenuCategoryData.objects.all(),
		'display':display}
	return render(request,'Menu.html',dic)
def singleblog(request):
	return render(request,'single-blog.html',{})
def adminproceedtopay(request):
	return render(request,'adminpages/proceedtopay.html',{})
def menucategory(request):
	return render(request,'menucategory.html',{})
def adminblockedcustomer(request):
	return render(request,'adminpages/blockedcustomer.html',{})
def admindeactivemenu(request):
	return render(request,'adminpages/deactivemenu.html',{})
def admindiscountcouponhistory(request):
	return render(request,'adminpages/discountcouponhistory.html',{})
@csrf_exempt
def adminlogincheck(request):
	if request.method=='POST':
		email=request.POST.get('email')
		password=request.POST.get('password')
		if email == 'admin@cafeliant.com' and password == AdminData.objects.all()[0].Admin_Password:
			request.session['admin'] = email
			return redirect('/adminindex/')
		elif email == 'manager@cafeliant.com' and password == ManagerData.objects.all()[0].Manager_Password:
			request.session['admin'] = email
			return redirect('/adminindex/')
		else:
			return HttpResponse("<script>alert('Incorrect Credentials'); window.location.replace('/adminlogin/')</script>")
	else:
		return redirect('/index/')
def adminindex(request):
	try:
		admin=request.session['admin']
		return render(request,'adminpages/index.html',{'checklogin':checklogin(admin)})
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
		menu=MenuData.objects.filter(Status='Active')
		dic={'data':MenuCategoryData.objects.all(),
			'menu':menu,
			'checklogin':checklogin(admin)}	
		return render(request,'adminpages/addmenuitem.html',dic)
	except:
		return redirect('/index/')
@csrf_exempt
def adminsavemenuitem(request):
	if request.method=='POST':
		name=request.POST.get('name')
		category=request.POST.get('category')
		price=request.POST.get('price')
		thumb=request.FILES['image']
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
			Item_Price=price,
			Item_Thumb=thumb
			)
		obj.save()
		menu=MenuData.objects.filter(Status='Active')
		dic={'data':MenuCategoryData.objects.all(),
			'msg':'Item Saved',
			'menu':menu,
			'checklogin':checklogin(request.session['admin'])}
		return render(request,'adminpages/addmenuitem.html',dic)
	else:
		return redirect('/index/')
def admineditmenuitem(request):
	try:
		admin=request.session['admin']
		name=request.GET.get('name')
		price=request.GET.get('price')
		discount=request.GET.get('discount')
		itemid=request.GET.get('Id')
		obj=MenuData.objects.filter(Item_ID=itemid)
		obj.update(Item_Name=name, Item_Price=price, Discount=discount)
		return redirect('/adminaddmenuitem/')
	except:
		return redirect('/index/')

def admindeletemenuitem(request):
	try:
		admin=request.session['admin']
		itemid=request.GET.get('Id')
		obj=MenuData.objects.filter(Item_ID=itemid).update(Status='Deactive')
		return redirect('/adminaddmenuitem/')
	except:
		return redirect('/index/')

def adminmenulist(request):
	try:
		admin=request.session['admin']
		dic={'data':MenuData.objects.all(),'checklogin':checklogin(admin)}
		return render(request,'adminpages/menulist.html',dic)
	except:
		return redirect('/index/')
def adminaddmenucategory(request):
	try:
		admin=request.session['admin']
		dic={'data':MenuCategoryData.objects.all(),'checklogin':checklogin(admin)}
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
				'msg':'Category Already Exists','checklogin':checklogin(request.session['admin'])}
			return render(request,'adminpages/addmenucategory.html',dic)
		else:
			obj.save()
			dic={'data':MenuCategoryData.objects.all(),
				'msg':'Saved!','checklogin':checklogin(request.session['admin'])}
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
	try:
		admin=request.session['admin']
		return render(request,'adminpages/adddiscountcoupon.html',{'checklogin':checklogin(request.session['admin'])})
	except:
		return redirect('/index/')
def admindiscountcouponlist(request):
	try:
		admin=request.session['admin']
		data=DiscountCouponData.objects.all()
		return render(request,'adminpages/discountcouponlist.html',{'data':data,'checklogin':checklogin(request.session['admin'])})
	except:
		return redirect('/index/')
def adminongoingorder(request):
	try:
		admin=request.session['admin']
		dic={'ordermenudata':OrderMenuData.objects.all(),
			'items':MenuData.objects.filter(Status='Active'),
			'orderdata':OrderData.objects.filter(Status='Active'),
			'category':MenuCategoryData.objects.all(),
			'checklogin':checklogin(request.session['admin'])}
		return render(request,'adminpages/ongoingorder.html',dic)
	except:
		return redirect('/index/')
@csrf_exempt
def admincreateorder(request):
	if request.method=='POST':
		o="O00"
		x=1
		oid=o+str(x)
		while OrderData.objects.filter(Order_ID=oid).exists():
			x=x+1
			oid=o+str(x)
		x=int(x)
		obj=OrderData(Order_ID=oid).save()
		for x in MenuData.objects.all():
			if not request.POST.get(x.Item_ID) == None:
				obj=OrderMenuData(Item_ID=request.POST.get(x.Item_ID),Order_ID=oid).save()
		dic={'items':MenuData.objects.all(),
			 'category':MenuCategoryData.objects.all(),
			 'orderdata':OrderData.objects.filter(Status='Active'),
			 'ordermenudata':OrderMenuData.objects.all(),
			 'checklogin':checklogin(request.session['admin']),
			'msg':'Order '+oid+' Created Successfully and Added to the Below List'}
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
				price=applyitemdiscount(y.Item_ID)
				total=total+(price*int(x.Quantity))
		
		tax=''
		for x in TaxData.objects.all():
			tax=x.Tax
		taxamount=(int(total)/100)*int(tax)
		amountwithtax=taxamount+int(total)
		dic={'customers':CustomerData.objects.all(),
			'orderid':oid,
			'totalamount':str(total),
			'taxamount':amountwithtax,'checklogin':checklogin(request.session['admin'])}
		return render(request,'adminpages/searchcustomer.html',dic)
	except:
		return redirect('/index/')

def admincustomersearchresult(request):
	try:
		admin=request.session['admin']
		cmobile=request.GET.get('cmobile')
		result=CustomerData.objects.filter(Mobile=cmobile)
		oid=request.session['orderid']
		total=0
		if CustomerData.objects.filter(Mobile=cmobile).exists():
			for x in CustomerData.objects.filter(Mobile=cmobile):
				OrderData.objects.filter(Order_ID=oid).update(Customer_ID=x.Customer_ID)
			for x in OrderMenuData.objects.filter(Order_ID=oid):
				for y in MenuData.objects.filter(Item_ID=x.Item_ID):
					price=applyitemdiscount(y.Item_ID)
					total=total+(price*int(x.Quantity))
			tax=''
			for x in TaxData.objects.all():
				tax=x.Tax
			taxamount=(int(total)/100)*int(tax)
			amountwithtax=taxamount+int(total)
			dic={'customers':CustomerData.objects.all(),
				'result':result,
				'orderid':oid,
				'taxamount':amountwithtax,
				'totalamount':str(total),
				'checklogin':checklogin(request.session['admin'])}
			return render(request,'adminpages/searchcustomer.html',dic)
		else:
			for x in OrderMenuData.objects.filter(Order_ID=oid):
				for y in MenuData.objects.filter(Item_ID=x.Item_ID):
					price=applyitemdiscount(y.Item_ID)
					total=total+(price*int(x.Quantity))
			tax=''
			for x in TaxData.objects.all():
				tax=x.Tax
			taxamount=(int(total)/100)*int(tax)
			amountwithtax=taxamount+int(total)
			dic={'customers':CustomerData.objects.all(),
				'cmobile':cmobile,
				'orderid':oid,
				'taxamount':amountwithtax,
				'msg':'No Customer Record Found, Add Customer Detail Below.',
				'totalamount':str(total),
				'checklogin':checklogin(request.session['admin'])}
			return render(request,'adminpages/searchcustomer.html',dic)
	except:
		return redirect('/index/')
@api_view(['GET'])
@csrf_exempt
def Apply_Promocode(request):
	amount=request.GET.get('amount')
	promo=request.GET.get('promo')
	amount=float(amount)
	applied_amount = applypromocode(promo, amount)
	dic = {'Response':'Success','amount':applied_amount, 'promo':promo}
	response_ = Response(dic)
	return response_

@csrf_exempt
def admincompletepayment(request):
	if request.method=='POST':
		paymode=request.POST.get('paymode')
		oid=request.session['orderid']
		amount=request.POST.get('amount')
		amountpaid=request.POST.get('finalamount')
		
		mobile=request.POST.get('mobile')
		name=request.POST.get('name')
		email=request.POST.get('email')
		address=request.POST.get('address')
		state=request.POST.get('state')
		city=request.POST.get('city')
		
		promo=request.POST.get('promo')
		transid=request.POST.get('transid')
		
		tax=TaxData.objects.all()[0].Tax
		taxamount=(int(amount[0:len(amount)-3])/100)*int(tax)
		amountwithtax=taxamount+int(amount[0:len(amount)-3])
		
		if CustomerData.objects.filter(Mobile=mobile).exists():
			dic=SavePayData(request, oid, tax, amount, amountwithtax, taxamount, amountpaid, transid, paymode, promo)
			dic.update({'checklogin':checklogin(request.session['admin'])})
			return render(request,'adminpages/bilinginvoice.html',dic)
		else:
			c="CUS00"
			x=1
			cid=c+str(x)
			while CustomerData.objects.filter(Customer_ID=cid).exists():
				x=x+1
				cid=c+str(x)
			x=int(x)
			if not name == '' and email == '' and address == '' and city == '' and state == '':
				obj=CustomerData(
					Customer_ID=cid,
					Name=name,
					Mobile=mobile,
					Email=email,
					Address=address,
					City=city,
					State=state
					)
				obj.save()
			else:
				obj=CustomerData(
					Customer_ID=cid,
					Mobile=mobile
					)
				obj.save()
			OrderData.objects.filter(Order_ID=oid).update(Customer_ID=cid)
			dic=SavePayData(request, oid, tax, amount, amountwithtax, taxamount, amountpaid, transid, paymode, promo)
			dic.update({'checklogin':checklogin(request.session['admin'])})
			return render(request,'adminpages/bilinginvoice.html',dic)

def adminorderhistory(request):
	try:
		admin=request.session['admin']
		dic={'data':OrderData.objects.filter(Status='Paid'),'checklogin':checklogin(request.session['admin'])}
		return render(request,'adminpages/orderhistory.html',dic)
	except:
		return redirect('/index/')
def adminpaymenthistory(request):
	try:
		admin=request.session['admin']
		dic={'checklogin':checklogin(request.session['admin']),'data':PaymentData.objects.all()}
		return render(request,'adminpages/paymenthistory.html',dic)
	except:
		return redirect('/index/')
def admincustomerlist(request):
	try:
		admin=request.session['admin']
		dic={'data':CustomerData.objects.all(),'checklogin':checklogin(request.session['admin'])}
		return render(request,'adminpages/customerlist.html',dic)
	except:
		return redirect('/index/')

def admintax(request):
	try:
		admin=request.session['admin']
		dic={'data':TaxData.objects.all(),'checklogin':checklogin(request.session['admin'])}
		return render(request,'adminpages/tax.html',dic)
	except:
		return redirect('/index/')

@csrf_exempt
def adminupdatetax(request):
	if request.method=='POST':
		TaxData.objects.all().update(Tax=request.POST.get('tax'))
		return redirect('/admintax/')
def admincoincount(request):
	try:
		admin=request.session['admin']
		dic={'data':CoinsData.objects.all(),'checklogin':checklogin(request.session['admin'])}
		return render(request,'adminpages/coinscount.html',dic)
	except:
		return redirect('/index/')
@csrf_exempt
def adminupdatecoincount(request):
	if request.method=='POST':
		CoinsData.objects.all().update(Coins_Count=request.POST.get('count'))
		return redirect('/admincoincount/')
def adminitemdiscount(request):
	try:
		admin=request.session['admin']
		dic={'data':MenuData.objects.filter(Status='Active'),'checklogin':checklogin(request.session['admin'])}
		return render(request,'adminpages/itemdiscount.html',dic)
	except:
		return redirect('/index/')
@csrf_exempt
def adminsaveitemdiscount(request):
	if request.method=='POST':
		admin=request.session['admin']
		MenuData.objects.filter(Item_ID=request.POST.get('itemid')).update(Discount=request.POST.get('discount'))
		return redirect('/adminitemdiscount/')
	else:
		return redirect('/index/')
def printinvoice(request):
	try:
		admin=request.session['admin']
		orderid=request.GET.get('orderid')
		orderdata=InvoiceData.objects.filter(Order_ID=orderid)[0]
		dic={'orderid':orderid,
			'gst':orderdata.TaxAmount,
			'tax':orderdata.Tax,
			'date':orderdata.Date,
			'amount':orderdata.Amount,
			'taxamount':orderdata.AmountwithTax,
			'payid':orderdata.Pay_ID,
			'promo':orderdata.Promocode,
			'amountpaid':orderdata.AmountPaid,
			'paymode':orderdata.PayMode,
			'menu':OrderMenuData.objects.filter(Order_ID=orderid),
			'items':GetOrderMenuList(orderid),
			'checklogin':checklogin(request.session['admin']),
			'customerdata':CustomerData.objects.filter(Customer_ID=orderdata.Customer_ID)}
		return render(request,'adminpages/bilinginvoice.html',dic)
	except:
		return redirect('/index/')
@csrf_exempt
def adminsettable(request):
	if request.method=='POST':
		orderid=request.POST.get('orderid')
		table=request.POST.get('table')
		OrderData.objects.filter(Order_ID=orderid).update(Table_No=table)
		return redirect('/adminongoingorder/')
	else:
		return redirect('/index/')

def adminmailbill(request):
	return render(request,'adminpages/mailbill.html',{})
def dashboard(request):
	return render(request,'dashboard.html',{})
@csrf_exempt
def savecoupon(request):
	if request.method=='POST':
		name=request.POST.get('name')
		code=request.POST.get('code')
		percent=request.POST.get('percent')
		o="DIS00"
		x=1
		oid=o+str(x)
		while DiscountCouponData.objects.filter(Coupon_ID=oid).exists():
			x=x+1
			oid=o+str(x)
		x=int(x)
		DiscountCouponData(Coupon_ID=oid,
							Coupon_Name=name,
							Coupon_Code=code,
							Discount_Percentage=percent).save()
		dic={'msg':'Saved Successfully','checklogin':checklogin(request.session['admin'])}
		return render(request,'adminpages/adddiscountcoupon.html',dic)
@csrf_exempt
def admindeletecoupon(request):
	try:
		admin=request.session['admin']
		cid=request.GET.get('cid')
		DiscountCouponData.objects.filter(Coupon_ID=cid).delete()
		return redirect('/admindiscountcouponlist/')
	except:
		return redirect('/index/')
def adminchangemanager(request):
	try:
		admin=request.session['admin']
		password=ManagerData.objects.all()[0].Manager_Password
		return render(request,'adminpages/changemanager.html',{'checklogin':checklogin(request.session['admin']),'password':password})
	except:
		return redirect('/index/')
@csrf_exempt
def adminsavemanagerpassword(request):
	try:
		admin=request.session['admin']
		newpassword=request.POST.get('newpassword')
		adminpassword=request.POST.get('adminpassword')
		if adminpassword==AdminData.objects.all()[0].Admin_Password:
			ManagerData.objects.all().delete()
			ManagerData(Manager_Password=newpassword).save()
			password=ManagerData.objects.all()[0].Manager_Password
			return render(request,'adminpages/changemanager.html',{'checklogin':checklogin(request.session['admin']),'msg':'Changed Successfully','password':password})
		else:
			return render(request,'adminpages/changemanager.html',{'checklogin':checklogin(request.session['admin']),'msg':'Incorrect Admin Password'})
	except:
		return redirect('/index/')
def adminchangeadmin(request):
	try:
		admin=request.session['admin']
		return render(request,'adminpages/changeadmin.html',{'checklogin':checklogin(admin)})
	except:
		return redirect('/index/')
@csrf_exempt
def adminsaveadmin(request):
	try:
		admin=request.session['admin']
		old=request.POST.get('oldpassword')
		new=request.POST.get('newpassword')
		if old==AdminData.objects.all()[0].Admin_Password:
			AdminData.objects.all()
			AdminData(Admin_Password=new).save()
			return render(request,'adminpages/changeadmin.html',{'msg':'Password Changed Successfully','checklogin':checklogin(admin)})
		else:
			return render(request,'adminpages/changeadmin.html',{'msg':'Incorrect Old Password','checklogin':checklogin(admin)})
	except:
		return redirect('/index/')

@csrf_exempt
def sendcontachform(request):
	if request.method=='POST':
		msg = request.POST.get('message')
		name = request.POST.get('name')
		email = request.POST.get('email')
		subject = request.POST.get('subject')
		print(email)
		msg = '''Query By : '''+name+'''('''+email+'''),
'''+msg
		email=EmailMessage(subject,msg,to=['liantcafe@gmail.com'])
		email.send()
		msg = '''Hi there!
We got your message, we will contact you soon!'''
		subject = 'Cafe Liant - Message Received'
		email = request.POST.get('email')
		email=EmailMessage(subject,msg,to=[email])
		email.send()
		return redirect('/index/')
	else:
		return redirect('/index/')