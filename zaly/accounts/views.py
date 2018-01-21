from datetime import datetime

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse


from  django.conf import settings

from django.utils.translation import ugettext as _


from django.contrib.auth import  get_user_model
from django.contrib import messages
from django.contrib import auth as auth_c


from .forms import ConnexionForm

User = get_user_model()


# Create your views here.



def login(request):
	error = False

	# if request.method=="POST":
	# 	username = request.POST["username"]
	# 	password = request.POST["password"]

	# 	user = auth_c.authenticate(username=username,password=password)
	# 	if user:
	# 		auth_c.login(request, user)
	# 		return redirect(reverse("home"))

	# 	else:
	# 		error = True
	form = ConnexionForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data["username"]
		password = form.cleaned_data["password"]


		user = auth_c.authenticate(username=username, password=password)

		if user:
			auth_c.login(request, user)
			messages.success(request, _("Bienvenu  {}".format(username)))
			return redirect(reverse("home"))


		else:
			error = True
	else:
		form = ConnexionForm()

	context = {
	    "form":form,
	    "error":error,
	}


	return render(request, "accounts/login.html", context)
