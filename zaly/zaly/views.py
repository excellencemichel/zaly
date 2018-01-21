from django.shortcuts import render



def home(request):
	return render(request, "home.html")




def detail(request):

	context = {}
	return render(request, "detail.html", context)