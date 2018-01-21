from django.shortcuts import render, get_object_or_404

from django.core.signals import request_finished, request_started #Pour la gestion des signaux
from django.dispatch import receiver

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .forms import ProduitForm, ProduitModelForm

from .models import Produit

# Create your views here.


def p_home(request):
	return render(request, "produits/p_home.html")





def my_callback(sender, **kwargs):
	"""
	Cette fonction est une fonction receptrice de signal
	le paramètre 'sender' represente le signal auquel la
	fonction sera connectée
	la paramètre générique nommé '**kwargs' sert à captérer
	les éventuelles paramètre nommés que le signal peut envoyer
	"""

	print("La requête vient de terminer")



#Ici c'est la connexion de la fonction receptrice de signal au signal
#A noter qu'il y a deux manière de connecter une fonction receptrice
# à un signal dont voici la première
# un peu en bas la seconde manière à travers le décorateur receiver
request_finished.connect(my_callback)



@receiver(request_started)#Le décorateur prend en paramètre le signal auquel la fonction receptrice doit réagir
def fonction_rapel(sender, **kwargs):
	print("Quand la requête http commence tu me mets ce message")



def create_produit_simple(request):

	form = ProduitForm(request.POST or None)
	if form.is_valid():
		data = form.cleaned_data
		title = data.get("title")
		description = data.get("description")
		price = data.get("price")

		new_produit = Produit(title=title, description=description, price=price).save()
	template = "produits/create_produit_old.html"
 
	context = {
		"form": form
	}

	return render(request, template, context)


def create_produit(request):
	form = ProduitModelForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save



	context = {
		"form":form,
		"submit_btn": "Create produit",
	}

	return render(request, "produits/form.html", context)



def update_produit(request, object_id =None, slug=None):
	produit = get_object_or_404(Produit, id=object_id, slug=slug)
	form = ProduitModelForm(request.POST or None, instance=produit)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	context = {
		"form" :form,
		"object":produit,
		"submit_btn" : "Update produit",
	}


	return render(request, "produits/form.html", context)


def detail_produit(request, object_id, slug):
	produit = get_object_or_404(Produit, id=object_id, slug=slug)

	context = {
		"produit": produit,
	}

	return render(request, "produits/detail_produit.html",  context )




class ProduitListView(ListView):
	model = Produit
	template_name = "produits/list_view.html"

	def get_context_data(self, **kwargs):
		context = super(ProduitListView, self).get_context_data(**kwargs)
		print (context)
		return context

	def get_queryset(self, *args, **kwargs):
		qs = super(ProduitListView, self).get_queryset(**kwargs)
		qs = qs.filter(title__icontains="Telephone")
		return qs




class ProduitDetailView(DetailView):
	model = Produit