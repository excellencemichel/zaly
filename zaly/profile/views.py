from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.urls import reverse

from django.template.loader import get_template, render_to_string

from django.conf import settings

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext as _

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site




from .tokens import account_activation_token
from .forms import UserCreationForm, ConnexionForm, ProfileUserChangeForm

User = get_user_model()

# Create your views here.


def home(request):
	return render(request, "profile/home.html")



"""
def base(request):
	return render(request, "base.html")

"""

def register(request):
	if request.method=="POST":
		form = UserCreationForm(request.POST or None, request.FILES or None)

		if form.is_valid():
			user = form.save(commit=False)

			user.is_active = False
			user.save()
			messages.success(request, _("Votre compte a été, un email vous a été envoyé pour pouvoir activer le compte."))


			current_site = get_current_site(request)
			message = render_to_string("profile/acc_active_email.html", {
				"user": user,
				"domain": current_site.domain,
				"uid": urlsafe_base64_encode(force_bytes(user.pk)),
				"token": account_activation_token.make_token(user),
				})
			mail_subject = "Nous vous remercions de nous avoir placé votre confiance en vous incrivant sur nimbacom"
			to_email = form.cleaned_data.get("email")
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			return HttpResponse("Please confirmez votre email pour completer l'inscription")

			# subject = "Nous vous remercions de nous avoir placé votre confiance en vous incrivant sur nimbacom"
			# from_email = settings.EMAIL_HOST_USER
			# to_email = form.cleaned_data["email"]
			# with open(settings.BASE_DIR + "/profile/templates/profile/sign_up_email.txt") as f:
			# 	signup_message = f.read()

			# message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=[to_email])
			# html_template = get_template("profile/sign_up_email.html").render()
			# message.attach_alternative(html_template, "text/html")
			# message.send()
			# return HttpResponse("Please confirmez votre email pour completer l'inscription")

			# return redirect(reverse(home))

	else :
		form = UserCreationForm()

	context = {
	   "form" : form,
	}


	return render(request, "profile/register.html", context)


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)

	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user =None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		return HttpResponse("Thank you for your email confirmation. Now you can login your account.")

	else:
		return HttpResponse("Activation link is invalid !")


@login_required
def qlq(request):
	return render(request, "profile/qlq.html")


# def connexion(request):
# 	error = False

# 	if request.method=="POST":
# 		form = ConnexionForm(request.POST)
# 		if form.is_valid():
# 			username = form.cleaned_data["username"]
# 			password = form.cleaned_data["password"]


# 			user = authenticate(username=username, password=password)

# 			if user:
# 				login(request, user)
# 				return redirect(reverse("home"))

# 			else:
# 				error = True
# 	else:
# 		form = ConnexionForm()

# 	context = {
# 	    "form": form,
# 	    "error":error,
# 	}

# 	return render(request, "profile/login.html",context)





@login_required
def update_user(request):
	if request.method=="POST":
		form = ProfileUserChangeForm(request.POST or None, request.FILES or None)

		if form.is_valid():
			form.save()
			return redirect(reverse(home))

	else:
		form = ProfileUserChangeForm()


	context = {
	    "form": form,
	}

	return render(request, "profile_user/update_user.html", context)

# @login_required
# def change_password(request):
# 	error = False
# 	if request.method=="POST":
# 		form = PasswordChangeForm(data=request.POST, user=request.user)
# 		if form.is_valid():
# 			form.save()
# 			update_session_auth_hash(request, form.user)
# 			return redirect(home)

# 		else:
# 			error = True


# 	else:
# 		form = PasswordChangeForm(user=request.user)

# 	context = {
# 	   "form":form,
# 	   "error":error,
# 	}

# 	return render(request, "profile/change_password.html", context)




# def logout(request):
# 	logout(request)
# 	return redirect(reverse("account_login"))