from django.db import models
from datetime import date
from django.conf import settings
# Create your models here.

class MenuData(models.Model):
	Add_Date=models.DateTimeField(auto_now=True)
	Item_ID=models.CharField(max_length=50, primary_key=True)
	Item_Category=models.CharField(max_length=20)
	Item_Name=models.CharField(max_length=50)
	Item_Price=models.CharField(max_length=10)
	class Meta:
		db_table="MenuData"

class MenuCategoryData(models.Model):
	Add_Date=models.DateTimeField(auto_now=True)
	Category_ID=models.CharField(max_length=50, primary_key=True)
	Category_Name=models.CharField(max_length=50)
	class Meta:
		db_table="MenuCategoryData"