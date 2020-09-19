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
def adminproceedtopay(request):
	return render(request,'adminpages/proceedtopay.html',{})
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
		menu=MenuData.objects.filter(Status='Active')
		dic={'data':MenuCategoryData.objects.all(),
			'menu':menu}	
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
		menu=MenuData.objects.filter(Status='Active')
		dic={'data':MenuCategoryData.objects.all(),
			'msg':'Item Saved',
			'menu':menu}
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
		return redirect('/adminaddmenuitem/')
	except:
		return redirect('/index/')

def admindeletemenuitem(request):
	try:
		admin=request.session['admin']
		itemid=request.GET.get('Id')
		print(itemid)
		obj=MenuData.objects.filter(Item_ID=itemid).update(Status='Deactive')
		return redirect('/adminaddmenuitem/')
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
	try:
		admin=request.session['admin']
		return render(request,'adminpages/adddiscountcoupon.html',{})
	except:
		return redirect('/index/')
def admindiscountcouponlist(request):
	try:
		admin=request.session['admin']
		data=DiscountCouponData.objects.all()
		return render(request,'adminpages/discountcouponlist.html',{'data':data})
	except:
		return redirect('/index/')
def adminongoingorder(request):
	try:
		admin=request.session['admin']
		dic={'ordermenudata':OrderMenuData.objects.all(),
			'items':MenuData.objects.all(),
			'orderdata':OrderData.objects.filter(Status='Active'),
			'category':MenuCategoryData.objects.all()}
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
			'taxamount':amountwithtax}
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
				'totalamount':str(total)}
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
				'totalamount':str(total)}
			return render(request,'adminpages/searchcustomer.html',dic)
	except:
		return redirect('/index/')
@csrf_exempt
def admincompletepayment(request):
	if request.method=='POST':
		paymode=request.POST.get('paymode')
		oid=request.session['orderid']
		amount=request.POST.get('amount')
		name=request.POST.get('name')
		mobile=request.POST.get('mobile')
		email=request.POST.get('email')
		address=request.POST.get('address')
		state=request.POST.get('state')
		city=request.POST.get('city')
		tax=''
		for x in TaxData.objects.all():
			tax=x.Tax
		taxamount=(int(amount[0:len(amount)-3])/100)*int(tax)
		amountwithtax=taxamount+int(amount[0:len(amount)-3])
		if CustomerData.objects.filter(Mobile=mobile).exists():
			if paymode=='Cash':
				dic={'amount':amount,
					'taxamount':amountwithtax,
					'mode':'Cash',
					'orderid':oid}
				return render(request,'adminpages/paybycash.html',dic)
			elif paymode=='Card':
				dic={'amount':amount,
					'taxamount':amountwithtax,
					'mode':'Card',
					'orderid':oid}
				return render(request,'adminpages/paybycard.html',dic)
			elif paymode=='QR':
				dic={'amount':amount,
					'taxamount':amountwithtax,
					'mode':'QR',
					'orderid':oid}
				return render(request,'adminpages/paybyqr.html',dic)
		else:
			o="CUS00"
			x=1
			oid=o+str(x)
			while CustomerData.objects.filter(Customer_ID=oid).exists():
				x=x+1
				oid=o+str(x)
			x=int(x)
			obj=CustomerData(
				Customer_ID=oid,
				Name=name,
				Mobile=mobile,
				Email=email,
				Address=address,
				City=city,
				State=state
				)
			obj.save()
			OrderData.objects.filter(Order_ID=oid).update(Customer_ID=oid)
			if paymode=='Cash':
				dic={'amount':amount,
					'taxamount':amountwithtax,
					'mode':'Cash',
					'orderid':oid}
				return render(request,'adminpages/paybycash.html',dic)
			elif paymode=='Card':
				dic={'amount':amount,
					'taxamount':amountwithtax,
					'mode':'Card',
					'orderid':oid}
				return render(request,'adminpages/paybycard.html',dic)
			elif paymode=='QR':
				dic={'amount':amount,
					'taxamount':amountwithtax,
					'mode':'QR',
					'orderid':oid}
				return render(request,'adminpages/paybyqr.html',dic)
@csrf_exempt
def admingeneratebill(request):
	if request.method=='POST':
		orderid=request.POST.get('orderid')
		amount=request.POST.get('amount')
		mode=request.POST.get('mode')
		promo=request.POST.get('promo').upper()
		o="PAY00"
		x=1
		oid=o+str(x)
		while PaymentData.objects.filter(Pay_ID=oid).exists():
			x=x+1
			oid=o+str(x)
		x=int(x)
		cusid=''
		tax=''
		for x in TaxData.objects.all():
			tax=x.Tax
		taxamount=(int(amount[0:len(amount)-3])/100)*int(tax)
		amountwithtax=taxamount+int(amount[0:len(amount)-3])
		for x in OrderData.objects.filter(Order_ID=orderid):
			cusid=x.Customer_ID
			if not mode=='Cash':
				amountwithpromo=applypromocode(promo, amountwithtax)
				obj=PaymentData(
					Pay_ID=oid,
					Order_ID=orderid,
					Customer_ID=x.Customer_ID,
					PayMode=mode,
					Receipt_Number=request.POST.get('reciept'),
					Amount=amount,
					Promocode=promo,
					AmountwithTax=amountwithtax,
					AmountPaid=amountwithpromo
				)
				obj.save()
				OrderData.objects.filter(Order_ID=orderid).update(Status='Paid',Pay_ID=oid)
			else:
				amountwithpromo=applypromocode(promo, amountwithtax)
				obj=PaymentData(
					Pay_ID=oid,
					Order_ID=orderid,
					Customer_ID=x.Customer_ID,
					PayMode=mode,
					Amount=amount,
					Promocode=promo,
					AmountwithTax=amountwithtax,
					AmountPaid=amountwithpromo
				)
				obj.save()
				OrderData.objects.filter(Order_ID=orderid).update(Status='Paid',Pay_ID=oid)
		CustomerData.objects.filter(Customer_ID=cusid).update(Coins_Wallet=(str(int(CustomerData.objects.filter(Customer_ID=cusid)[0].Coins_Wallet)+round(int(amountwithtax)/100)*int(CoinsData.objects.all()[0].Coins_Count))))
		coins=str(round(int(amountwithtax)/100)*int(CoinsData.objects.all()[0].Coins_Count))
		totalcoins=(str(int(CustomerData.objects.filter(Customer_ID=cusid)[0].Coins_Wallet)+round(int(amountwithtax)/100)*int(CoinsData.objects.all()[0].Coins_Count)))
		sendbillemail(CustomerData.objects.filter(Customer_ID=cusid), orderid, oid, mode, str(datetime.date.today()), GetOrderMenuList(orderid), str(taxamount/2), str(int(tax)/2), amount, amountwithtax, coins, str(totalcoins))
		InvoiceData(
			Order_ID=orderid,
			Customer_ID=cusid,
			TaxAmount=str(taxamount/2),
			Tax=str(int(tax)/2),
			Date=datetime.date.today(),
			AmountwithTax=amountwithtax,
			Amount=amount,
			Promocode=promo,
			AmountPaid=amountwithpromo,
			Pay_ID=oid,
			PayMode=mode
		).save()
		dic={'orderid':orderid,
			'gst':taxamount/2,
			'tax':int(tax)/2,
			'date':datetime.date.today(),
			'amount':amount,
			'taxamount':amountwithtax,
			'amountpaid':amountwithpromo,
			'promo':promo,
			'payid':oid,
			'paymode':mode,
			'menu':OrderMenuData.objects.filter(Order_ID=orderid),
			'items':GetOrderMenuList(orderid),
			'customerdata':CustomerData.objects.filter(Customer_ID=cusid)}
		return render(request,'adminpages/bilinginvoice.html',dic)
def adminorderhistory(request):
	try:
		admin=request.session['admin']
		dic={'data':OrderData.objects.filter(Status='Paid')}
		return render(request,'adminpages/orderhistory.html',dic)
	except:
		return redirect('/index/')
def adminpaymenthistory(request):
	try:
		admin=request.session['admin']
		dic={'data':PaymentData.objects.all()}
		return render(request,'adminpages/paymenthistory.html',dic)
	except:
		return redirect('/index/')
def admincustomerlist(request):
	try:
		admin=request.session['admin']
		dic={'data':CustomerData.objects.all()}
		return render(request,'adminpages/customerlist.html',dic)
	except:
		return redirect('/index/')

def admintax(request):
	try:
		admin=request.session['admin']
		dic={'data':TaxData.objects.all()}
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
		dic={'data':CoinsData.objects.all()}
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
		dic={'data':MenuData.objects.filter(Status='Active')}
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
		dic={'msg':'Saved Successfully'}
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