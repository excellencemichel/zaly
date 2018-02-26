import datetime

from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import View 
from django.shortcuts import render


#Local

from zaly.mixins import AjaxRequiredMixin
from produits.models import (
					Produit, 
					MyProduits


					)

from billing.models import Transaction
# Create your views here.



class CheckoutTestView(View):

	def post(self, request, *args, **kwargs):
		print(request.POST.get("testData"))
		if request.is_ajax():
			print(request.user.is_authenticated)
			if not request.user.is_authenticated:
				data = {
				"works" : False,
				}
				return JsonResponse(data, status=401)
			# raise Http404

			data = {
			"works" : True,
			'time': datetime.datetime.now(),
				}
			return JsonResponse(data)
		return HttpResponse("Hello World !")
	def get(self, request, *args, **kwargs):
		context = {}

		template = "checkout/test.html"
		return render (request, template, context)




class CheckoutAjaxView(AjaxRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return JsonResponse({}, status=401)

		# credit card required
		user = request.user
		produit_id = request.POST.get("produit_id")
		exists = Produit.objects.filter(id=produit_id).exists()
		if not exists:
			return JsonResponse({}, status=404)

		# produit_obj = Produit.objects.filter(id=produit_id).first()

		try:
			produit_obj = Produit.objects.get(id=produit_id)

		except:
			produit_obj = Produit.objects.filter(id=produit_id).first()

		#run transaction
		#assume it's succesful

		trans_obj = Transaction.objects.create(user=request.user,
											produit = produit_obj,
											price = produit_obj.get_price,
			)

		my_produits = MyProduits.objects.get_or_create(user=request.user)[0]
		my_produits.produits.add(produit_obj)
		
		# my_produits = MyProduits.objects.all()
		# print(type(my_produits))
		# print(type(produit_obj))
		download_link = produit_obj.get_download()
		preview_link = download_link + "?preview=True"
		data = {
		"download" : download_link,
		"preview" : preview_link,
		}
		return JsonResponse(data)


