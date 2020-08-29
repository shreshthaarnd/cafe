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
				'rate':str(applyitemdiscount(y.Item_ID)),
				'quantity':x.Quantity,
				'total':int(x.Quantity)*int(y.Item_Price)}
		lt.append(dic)
	return lt
def applyitemdiscount(itemid):
	item=MenuData.objects.filter(Item_ID=itemid)[0]
	price=int(item.Item_Price)
	discountpercent=int(item.Discount)
	discount=(price/100)*discountpercent
	return int(price-discount)