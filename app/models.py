from django.db import models
from django.conf import settings

class MenuData(models.Model):
	Add_Date=models.DateTimeField(auto_now=True)
	Item_ID=models.CharField(max_length=50, primary_key=True)
	Item_Category=models.CharField(max_length=20)
	Item_Name=models.CharField(max_length=50)
	Item_Price=models.CharField(max_length=10)
	Status=models.CharField(max_length=10, default='Active')
	class Meta:
		db_table="MenuData"

class MenuCategoryData(models.Model):
	Add_Date=models.DateTimeField(auto_now=True)
	Category_ID=models.CharField(max_length=50, primary_key=True)
	Category_Name=models.CharField(max_length=50)
	class Meta:
		db_table="MenuCategoryData"

class OrderData(models.Model):
	Add_Date=models.DateTimeField(auto_now=True)
	Order_ID=models.CharField(max_length=100, primary_key=True)
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
	class Meta:
		db_table="PaymentData"