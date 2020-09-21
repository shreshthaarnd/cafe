from django.db import models
from django.conf import settings

class MenuData(models.Model):
	Add_Date=models.DateTimeField(auto_now=True)
	Item_ID=models.CharField(max_length=50, primary_key=True)
	Item_Category=models.CharField(max_length=20)
	Item_Name=models.CharField(max_length=50)
	Item_Price=models.CharField(max_length=10)
	Item_Thumb=models.FileField(upload_to='itemthumb/')
	Discount=models.CharField(max_length=10, default='0')
	Status=models.CharField(max_length=10, default='Active')
	class Meta:
		db_table="MenuData"

class MenuCategoryData(models.Model):
	Add_Date=models.DateTimeField(auto_now=True)
	Category_ID=models.CharField(max_length=50, primary_key=True)
	Category_Name=models.CharField(max_length=50)
	class Meta:
		db_table="MenuCategoryData"

class TaxData(models.Model):
	Tax=models.CharField(max_length=5)
	class Meta:
		db_table="TaxData"

class CoinsData(models.Model):
	Coins_Count=models.CharField(max_length=5)
	class Meta:
		db_table="CoinsData"

class OrderData(models.Model):
	Add_Date=models.DateTimeField(auto_now=True)
	Order_ID=models.CharField(max_length=100, primary_key=True)
	Table_No=models.CharField(max_length=50, default='Not Assigned')
	Customer_ID=models.CharField(max_length=50, default='Not Availiable')
	Pay_ID=models.CharField(max_length=50, default='Not Availiable')
	Status=models.CharField(max_length=50, default='Active')
	class Meta:
		db_table="OrderData"

class OrderMenuData(models.Model):
	Item_ID=models.CharField(max_length=50)
	Order_ID=models.CharField(max_length=100)
	Quantity=models.CharField(max_length=50, default="1")
	class Meta:
		db_table="OrderMenuData"

class CustomerData(models.Model):
	Add_Date=models.DateTimeField(auto_now=True)
	Customer_ID=models.CharField(max_length=50, primary_key=True)
	Name=models.CharField(max_length=100)
	Mobile=models.CharField(max_length=15)
	Email=models.CharField(max_length=50)
	Address=models.CharField(max_length=200, default='Not Availiable')
	City=models.CharField(max_length=20, default='Not Availiable')
	State=models.CharField(max_length=20, default='Not Availiable')
	Coins_Wallet=models.CharField(max_length=10, default='0')
	class Meta:
		db_table="CustomerData"

class PaymentData(models.Model):
	Add_Date=models.DateField(auto_now=True)
	Pay_ID=models.CharField(max_length=50, primary_key=True)
	Order_ID=models.CharField(max_length=100)
	Customer_ID=models.CharField(max_length=15)
	PayMode=models.CharField(max_length=10)
	Receipt_Number=models.CharField(max_length=50, default='NA if Cash')
	Amount=models.CharField(max_length=50)
	Promocode=models.CharField(max_length=50, default='Not Applied')
	AmountwithTax=models.CharField(max_length=50)
	AmountPaid=models.CharField(max_length=50, default='0')
	class Meta:
		db_table="PaymentData"

class InvoiceData(models.Model):
	Order_ID=models.CharField(max_length=100)
	Customer_ID=models.CharField(max_length=15)
	TaxAmount=models.CharField(max_length=10)
	Tax=models.CharField(max_length=10)
	Date=models.CharField(max_length=10)
	AmountwithTax=models.CharField(max_length=10)
	Amount=models.CharField(max_length=10)
	Promocode=models.CharField(max_length=50, default='Not Applied')
	AmountPaid=models.CharField(max_length=50, default='0')
	Pay_ID=models.CharField(max_length=10)
	PayMode=models.CharField(max_length=10)
	class Meta:
		db_table="InvoiceData"

class DiscountCouponData(models.Model):
	Coupon_ID=models.CharField(max_length=50, primary_key=True)
	Coupon_Name=models.CharField(max_length=50)
	Coupon_Code=models.CharField(max_length=50)
	Discount_Percentage=models.CharField(max_length=50)
	Used=models.CharField(max_length=10, default='0')
	Status=models.CharField(max_length=10, default='Active')
	class Meta:
		db_table="DiscountCouponData"