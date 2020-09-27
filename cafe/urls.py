from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminlogin/',adminlogin),
    path('adminlogincheck/',adminlogincheck),
    path('adminlogout/',adminlogout),
    path('adminindex/',adminindex),
    path('adminaddmenuitem/',adminaddmenuitem),
    path('adminsavemenuitem/',adminsavemenuitem),
    path('admineditmenuitem/',admineditmenuitem),
    path('admindeletemenuitem/',admindeletemenuitem),
    path('adminmenulist/',adminmenulist),
    path('adminaddmenucategory/',adminaddmenucategory),
    path('adminsavemenucategory/',adminsavemenucategory),
    path('admineditmenucategory/',admineditmenucategory),
    path('admindeletemenucategory/',admindeletemenucategory),
    path('adminadddiscountcoupon/',adminadddiscountcoupon),
    path('admindiscountcouponlist/',admindiscountcouponlist),
    path('adminongoingorder/',adminongoingorder),
    path('admincoincount/',admincoincount),
    path('adminitemdiscount/',adminitemdiscount),
    path('adminmailbill/',adminmailbill),
    path('index/',index),
    path('about/',about),
    path('blog/',blog),
    path('contact/',contact),
    path('elements/',elements),
    path('menu/',menu),
    path('singleblog/',singleblog),
    path('dashboard/',dashboard),
    path('admincreateorder/',admincreateorder),
    path('adminorderhistory/',adminorderhistory),
    path('adminproceedtopay/',adminproceedtopay),
    path('admincustomerlist/',admincustomerlist),
    path('adminsaveordermenu/',adminsaveordermenu),
    path('menucategory/',menucategory),
    path('adminblockedcustomer/',adminblockedcustomer),
    path('adminchangemanager/',adminchangemanager),
    path('admindeactivemenu/',admindeactivemenu),
    path('admindiscountcouponhistory/',admindiscountcouponhistory),
    path('adminpaymenthistory/',adminpaymenthistory),
    path('adminaddmoreitemstoorder/',adminaddmoreitemstoorder),
    path('admincancelorder/',admincancelorder),
    path('adminsearchcustomer/',adminsearchcustomer),
    path('admincustomersearchresult/',admincustomersearchresult),
    path('admincompletepayment/',admincompletepayment),
    path('admingeneratebill/',admingeneratebill),
    path('admintax/',admintax),
    path('adminupdatetax/',adminupdatetax),
    path('adminupdatecoincount/',adminupdatecoincount),
    path('adminsaveitemdiscount/',adminsaveitemdiscount),
    path('printinvoice/',printinvoice),
    path('adminsettable/',adminsettable),
    path('savecoupon/',savecoupon),
    path('admindeletecoupon/',admindeletecoupon),
    path('adminsavemanagerpassword/',adminsavemanagerpassword),
    path('adminchangeadmin/',adminchangeadmin),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
