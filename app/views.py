from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request,'index.html',{})
def about(request):
	return render(request,'about.html',{})
def chefs(request):
	return render(request,'chefs.html',{})
def contact(request):
	return render(request,'contact.html',{})
def elements(request):
	return render(request,'elements.html',{})
def foodmenu(request):
	return render(request,'food_menu.html',{})
def singleblog(request):
	return render(request,'single-blog.html',{})