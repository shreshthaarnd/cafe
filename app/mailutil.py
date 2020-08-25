from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders
from functools import lru_cache
import mimetypes

def billhtml(customerobj, orderid, payid, paymode, date, menuitems, taxamount, tax, amount, totalamount, coins, totalcoins):
	items=''
	for x in menuitems:
		items=items+'''<tr>
				<td>'''+x['sr']+'''</td>
				<td>'''+x['name']+'''</td>
				<td>'''+x['quantity']+'''</td>
				<td><i class="fa fa-inr"></i>'''+x['rate']+'''</td>
				<td><i class="fa fa-inr"></i>'''+str(x['total'])+'''</td>
			</tr>'''

	html='''<!doctype html>
<html>
<head>
	<title>Cafe Liant : Billing Invoice</title>
	<meta charset="utf-8">
	<meta http-euiv="X-A-Compatible" containt="IE-edge">
	<meta name="viewport" containt="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body>
	<div style="text-align:center;">
		<img src="http://srd.pythonanywhere.com/static/img/favicon.png">
		<h1>Billing Invoice</h1>
	</div>
	<div style="width:100%;padding:10px;float:left;">
		<p style="font-size:20px;">
			<span style="font-weight:bold;font-size:25px;">'''+customerobj[0].Name+'''</span><br>
			<span>'''+customerobj[0].Address+'''</span><br>
			<span>'''+customerobj[0].City+''', '''+customerobj[0].State+'''</span><br>
			<span>+91-'''+customerobj[0].Mobile+''', '''+customerobj[0].Email+'''</span>
			
		</p>
	</div>
	<div style="text-align:center;padding:10px;">
		<span style="text-align:center;font-size:20px;">Date : <span style="font-weight:bold;">'''+date+'''</span> | Order ID : <span style="font-weight:bold;">'''+orderid+'''</span> | Payment ID : <span style="font-weight:bold;">'''+payid+'''</span> | Payment Mode : <span style="font-weight:bold;">By '''+paymode+'''</span></span>
	</div>
	<div style="width:100%;padding:10px;">
		<table style="width:100%;text-align:center;font-size:20px;">
			<tr style="background-color:black;color:white;">
				<th>Sr No.</th>
				<th>Item Name</th>
				<th>Quantity</th>
				<th>Rate</th>
				<th>Amount</th>
			</tr>
			'''+items+'''
		</table>
	</div>
	<div style="padding:10px;">
		<table style="float:right;font-size:20px;font-weight:bold;">
			<tr>
				<td>Total : </td>
				<td><i class="fa fa-inr"></i>'''+amount+'''</td>
			</tr>
			<tr>
				<td>CGST '''+tax+'''% :</td>
				<td><i class="fa fa-inr"></i>'''+taxamount+'''</td>
			</tr>
			<tr>
				<td>SGST '''+tax+'''% :</td>
				<td><i class="fa fa-inr"></i>'''+taxamount+'''</td>
			</tr>
			<tr>
				<td>Total Including Tax :</td>
				<td><i class="fa fa-inr"></i>'''+str(totalamount)+'''</td>
			</tr>
		</table>
	</div>
	<div>
		<span style="font-size:20px;font-weight:bold;">You received '''+coins+''' Coins</span><br>
		<span style="font-size:25px;font-weight:bold;">Total Coins in Your Wallet '''+totalcoins+''' Coins</span>
	</div>
</body>
</html>'''
	return html

def sendbillemail(customerobj, orderid, payid, paymode, date, menuitems, taxamount, tax, amount, totalamount, coins, totalcoins):
	message = EmailMultiAlternatives(
    	subject='Cafe Liant - Billing Invoice for Order '+orderid,
    	body='',
    	from_email=settings.EMAIL_HOST_USER,
    	to=[customerobj[0].Email]
	)
	message.mixed_subtype = 'related'
	message.attach_alternative(billhtml(customerobj, orderid, payid, paymode, date, menuitems, taxamount, tax, amount, totalamount, coins, totalcoins), "text/html")
	message.send(fail_silently=False)