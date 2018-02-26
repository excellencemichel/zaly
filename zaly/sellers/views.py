from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import FormMixin




from zaly.mixins import (
			MultiSlugMixin, 
			SubmitBtnMixin,
			LoginRequiredMixin,
			StaffRequiredMixin,


			)

from .models import SellerAccount


from .forms import NewSellerForm


# Create your views here.




class SellerAccountDashboard(LoginRequiredMixin, FormMixin ,View):
	form_class  = NewSellerForm
	success_url = "/seller/"

	def post(self, request, *args, **kwargs):
		# self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)

		else:
			return self.form_invalid(form)
		# form = NewSellerForm(request.POST)
		# if form.is_valid():
		# 	print ("Make the user aplly model")
		# return render(request, "sellers/dashboard.html", {"form": form})


	def get(self, request, *args, **kwargs):
		apply_form = self.get_form() #NewSellerForm()

		account = SellerAccount.objects.filter(user=self.request.user)
		exists = account.exists()
		active = None

		context = {}

		if exists:
			account = account.first()
			active = account.active


		#if no exists, show form
		#if exists and no active, show pending
		#if exists and active, show dashbord data.

		if not exists and not active:
			context["title"]= "Apply for Account"
			context["apply_form"] = apply_form

		elif exists and not active:
			context["title"] = "Account Pending"

		elif exists and active:
			context["title"] = "Seller Dashbord"

		else:
			pass

		# context = {
		# 	"apply_form": apply_form,
		# 	"account" : account,
		# 	"active": active,
		# 	"exists": exists,
		# }
		return render(request, "sellers/dashboard.html" , context)



	def form_valid(self, form):
		valid_data = super(SellerAccountDashboard, self).form_valid(form)
		obj = SellerAccount.objects.create(user=self.request.user)
		print("Working :)")
		return valid_data

