import random

from django.shortcuts import render

from django.views.generic import View 

from produits.models import Produit


# Create your views here.


class DashboardView(View):

	def get(self, request, *args, **kwargs):

		tag_views = None
		produits = None
		top_tags = None
		owned = None
		try:
			tag_views = request.user.tagview_set.all().order_by("-count")[:5]

		except:
			pass

		try:
			owned = request.user.myproduits.produits.all()

		except:
			pass

		if tag_views:
			top_tags = [x.tag for x in tag_views]

			produits = Produit.objects.filter(tag__in=top_tags)
			if owned:
				produits = produits.exclude(pk__in=owned)

			if produits.count()<10:
				produits = Produit.objects.all().order_by("?")
				if owned:
					produits = produits.exclude(pk__in=owned)
				produits = produits[:10]

			else:
				produits = produits.distinct()
				produits = sorted(produits, key= lambda x: random.random())

		# produits = Produit.objects.all()
		# print(produits)

		context = {
					"produits" : produits,
					"top_tags": top_tags
		}
		return render(request, "dashboard/view.html",context)