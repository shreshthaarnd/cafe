from app.models import *
from app.mailutil import *
from app.sms import *
import datetime

def GetOrderMenuList(orderid):
	dic={}
	lt=[]
	count=0
	for x in OrderMenuData.objects.filter(Order_ID=orderid):
		for y in MenuData.objects.filter(Item_ID=x.Item_ID):
			count=count+1
			dic={'sr':str(count),
				'name':y.Item_Name,
				'rate':str(applyitemdiscount(y.Item_ID)),
				'quantity':x.Quantity,
				'discount':y.Discount,
				'total':float(x.Quantity)*float(applyitemdiscount(y.Item_ID))}
		lt.append(dic)
	return lt

def applyitemdiscount(itemid):
	item=MenuData.objects.filter(Item_ID=itemid)[0]
	price=float(item.Item_Price)
	discountpercent=float(item.Discount)
	discount=(price/100)*discountpercent
	return round(float(price-discount), 2)

def applypromocode(code, amount):
	if DiscountCouponData.objects.filter(Coupon_Code=code).exists():
		discount=DiscountCouponData.objects.filter(Coupon_Code=code)[0].Discount_Percentage
		disamount=(float(amount)/100)*int(discount)
		return round(float(amount)-disamount, 2)
	else:
		return amount

def checklogin(id):
	if id=='admin@cafeliant.com':
		return 'admin'
	elif id=='manager@cafeliant.com':
		return 'manager'
	else:
		return 'none'

def SavePayData(request, orderid, tax, amount, amountwithtax, taxamount, amountpaid, transid, mode, promo):
	amount = str(amount)
	o="PAY00"
	x=1
	oid=o+str(x)
	while PaymentData.objects.filter(Pay_ID=oid).exists():
		x=x+1
		oid=o+str(x)
	x=int(x)
	cusid=''
	for x in OrderData.objects.filter(Order_ID=orderid):
		cusid=x.Customer_ID
		if not mode=='Cash':
			if promo == '':
				obj=PaymentData(
					Pay_ID=oid,
					Order_ID=orderid,
					Customer_ID=x.Customer_ID,
					PayMode=mode,
					Receipt_Number=transid,
					Amount=amount,
					AmountwithTax=amountwithtax,
					AmountPaid=amountpaid
				)
				obj.save()
			else:
				obj=PaymentData(
					Pay_ID=oid,
					Order_ID=orderid,
					Customer_ID=x.Customer_ID,
					PayMode=mode,
					Receipt_Number=transid,
					Amount=amount,
					Promocode=promo,
					AmountwithTax=amountwithtax,
					AmountPaid=amountpaid
				)
				obj.save()
			OrderData.objects.filter(Order_ID=orderid).update(Status='Paid',Pay_ID=oid)
		else:
			if promo == '':
				obj=PaymentData(
					Pay_ID=oid,
					Order_ID=orderid,
					Customer_ID=x.Customer_ID,
					PayMode=mode,
					Amount=amount,
					AmountwithTax=amountwithtax,
					AmountPaid=amountpaid
				)
				obj.save()
			else:
				obj=PaymentData(
					Pay_ID=oid,
					Order_ID=orderid,
					Customer_ID=x.Customer_ID,
					PayMode=mode,
					Amount=amount,
					AmountwithTax=amountwithtax,
					Promocode=promo,
					AmountPaid=amountpaid
				)
				obj.save()
			OrderData.objects.filter(Order_ID=orderid).update(Status='Paid',Pay_ID=oid)
	customer = CustomerData.objects.filter(Customer_ID=cusid)
	customer.update(Coins_Wallet=(str(int(customer[0].Coins_Wallet)+round(int(amountwithtax)/100)*int(CoinsData.objects.all()[0].Coins_Count))))
	coins = str(round(float(amountpaid)/100)*int(CoinsData.objects.all()[0].Coins_Count))
	totalcoins = (str(int(customer[0].Coins_Wallet)+round(float(amountpaid)/100)*int(CoinsData.objects.all()[0].Coins_Count)))
	
	try:
		sendbillemail(customer, orderid, oid, mode, str(datetime.date.today()), GetOrderMenuList(orderid), str(taxamount/2), str(int(tax)/2), amount, amountpaid, coins, str(totalcoins))
	except:
		print('SMTPRecipientsRefused')
	
	#sendBillSMS(customer[0].Mobile, str(amountpaid), orderid, oid, coins)
	
	InvoiceData(
		Order_ID=orderid,
		Customer_ID=cusid,
		TaxAmount=str(taxamount/2),
		Tax=str(int(tax)/2),
		Date=datetime.date.today(),
		AmountwithTax=amountwithtax,
		Amount=amount,
		Promocode=promo,
		AmountPaid=amountpaid,
		Pay_ID=oid,
		PayMode=mode
	).save()
	
	if promo=='':
		promo=None
	dic={'orderid':orderid,
			'gst':round(taxamount/2, 2),
			'tax':round(float(tax)/2, 2),
			'date':datetime.date.today(),
			'amount':amount,
			'taxamount':amountwithtax,
			'amountpaid':amountpaid,
			'promo':promo,
			'payid':oid,
			'paymode':mode,
			'checklogin':checklogin(request.session['admin']),
			'menu':OrderMenuData.objects.filter(Order_ID=orderid),
			'items':GetOrderMenuList(orderid),
			'customerdata':CustomerData.objects.filter(Customer_ID=cusid)}
	return dic