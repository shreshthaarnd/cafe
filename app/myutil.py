from app.models import *

def GetOrderMenuList(orderid):
	dic={}
	lt=[]
	count=0
	for x in OrderMenuData.objects.filter(Order_ID=orderid):
		for y in MenuData.objects.filter(Item_ID=x.Item_ID):
			count=count+1
			dic={'sr':str(count),
				'name':y.Item_Name,
				'rate':y.Item_Price,
				'quantity':x.Quantity,
				'total':int(x.Quantity)*int(y.Item_Price)}
		lt.append(dic)
	return lt