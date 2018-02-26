import os
from mimetypes import guess_type

from django.conf import settings
# from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import HttpResponse, Http404, FileResponse

from django.core.signals import request_finished, request_started #Pour la gestion des signaux
from django.dispatch import receiver
from django.urls import reverse, reverse_lazy


from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from zaly.mixins import (
			MultiSlugMixin, 
			SubmitBtnMixin,
			LoginRequiredMixin,
			StaffRequiredMixin,


			)

from .mixins import ProduitManagerMixin

from .forms import ProduitForm, ProduitModelForm

from .models import Produit

from tags.models import Tag
from analytics.models import TagView

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

		new_produit = Produit(title=title, description=description, price=price)
		new_produit.save()

		return redirect (reverse("home"))


	template = "produits/create_produit.html"
 
	context = {
		"form": form
	}

	return render(request, template, context)


def create_produit(request):
	form = ProduitModelForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

		return redirect (reverse("home"))

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

		return redirect (reverse("home"))

	context = {
		"form" :form,
		"object":produit,
		"submit_btn" : "Update produit",
	}


	return render(request, "produits/form.html", context)


def detail_produit(request, object_id, slug):

	context = {}
	produit = get_object_or_404(Produit, id=object_id, slug=slug)

	filepath = os.path.join(settings.PROTECTED_ROOT, produit.media.path)
	route = filepath.split(".")
	extention = route[-1]
	# print(route)

	# print(type(filepath))


	print (extention)
	if extention == "jpg" or extention == "png" or extention == "gif":
		preview = True

		context["preview"] =preview

	elif extention != "jpg" or extention != "png" or extention != "gif":
		preview = False

		context["preview"] =preview


	context["produit"] =produit
	# print(context)

	return render(request, "produits/detail_produit.html",  context )




class ProduitListView(ListView):
	model = Produit
	template_name = "produits/list_view.html"

	def get_context_data(self, **kwargs):
		context = super(ProduitListView, self).get_context_data(**kwargs)
		# print (context)
		return context

	def get_queryset(self, *args, **kwargs):
		"""
		Cette fonction permet de n'obtenir dans l'affichage
		les objets qui remplissent les conditions définies ici
		-contains tient compte de casse(majuscule et miniscule)
		-icontains permet de passer au travers la casse
		-Et contains et icontains ne gèrent pas les accent,
		 Téléphone est différent de Telephone

		 l'ordonancement avec order_by()
		 	sans le signe moins devant avec les id c'est du plus ancien aux plus recents donc des petit id aux grands id
		 	avec le signe moins c'est maintenant du plus recent aux plus anciens donc des id grands aux id petits
		"""
		qs = super(ProduitListView, self).get_queryset(**kwargs).order_by("-id")
		query = self.request.GET.get("q")
		if query:	
			qs = qs.filter(
							Q(title__icontains=query)|
							Q(description__icontains=query)

						  ).order_by("id")
		return qs




class ProduitDetailView(MultiSlugMixin,DetailView):
	model = Produit


	def get_context_data(self, *args, **kwargs):

		context = super(ProduitDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		tags = obj.tag_set.all()
		for tag in tags:
			new_tag = TagView.objects.add_count(self.request.user, tag)
			# new_tag = TagView.objects.get_or_create(user=self.request.user,
			# 										tag=tag)[0]
			# new_tag.count +=1
			# new_tag.save()

		return  context




class ProduitCreateView(LoginRequiredMixin,CreateView, SubmitBtnMixin):

	model = Produit
	template_name = "produits/form.html"
	form_class = ProduitModelForm
	# success_url = reverse_lazy("home")

	submit_btn = "Create produit"

	def form_valid(self, form):
		user = self.request.user

		form.instance.user = user
		valid_data = super(ProduitCreateView, self).form_valid(form)
		form.instance.managers.add(user)

		tags = form.cleaned_data.get("tags")
		if tags:
			tags_list = tags.split(",")

			for tag in tags_list:
				if not tag == " ":
					new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
					new_tag.produits.add(form.instance)

		return valid_data


	def get_success_url(self):
		return reverse("produits:list")



class ProduitUpdateView(LoginRequiredMixin,MultiSlugMixin, SubmitBtnMixin, UpdateView):
	model = Produit

	template_name = "produits/form.html"
	form_class = ProduitModelForm
	# success_url = reverse_lazy("home")

	submit_btn = "Update produit"


	def get_initial(self):

		initial = super(ProduitUpdateView, self).get_initial()
		print(initial)
		tags = self.get_object().tag_set.all()

		initial["tags"] =  ", ".join([x.title for x in tags])

		return initial

	def form_valid(self, form):
		valid_data = super(ProduitUpdateView, self).form_valid(form)
		print(form.cleaned_data)
		tags = form.cleaned_data.get("tags")
		obj = self.get_object()
		obj.tag_set.clear()
		if tags:
			tags_list = tags.split(",")
			for tag in tags_list:
				if not tag == " ":

					new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
					new_tag.produits.add(self.get_object())
		return valid_data

	# def get_object(self, *args, **kwargs):
	# 	user = self.request.us																					²er
	# 	obj = super(ProduitUpdateView, self).get_object(*args, **kwargs)
	# 	if obj.user == user or user in obj.managers.all():
	# 		return obj

	# 	else:
	# 		# return HttpResponse("Tu n'es pas membre du club")
	# 		raise Http404
	# 		# return redirect (reverse_lazy("home"))



class ProduitDownloadView(MultiSlugMixin, DetailView):
	model = Produit

	def get(self, request, *args, **kwargs):
		"""
		Pour le téléchargement des fichier
		A noter que la methoe file proposée dans le cours pour ouvrir
		les fichier ne marche avec python 3
		c'est la méthode open avec l'option d'ouverture qui doit utiliser
		le b l'option bytes pour pouvoir acceder à l'encodage du fichier
		"""
		obj = self.get_object()
		if obj in request.user.myproduits.produits.all():

			filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
			route = filepath.split(".")
			extention = route[-1]
			# print(route)

			# print(type(filepath))
			guessed_type = guess_type(filepath)[0]
			# print(guessed_type)

			# wrapper = FileResponse(file(filepath)) #ça na marche que pour python2
			wrapper = FileResponse(open(filepath, "rb")) # A ne pas oublier le b pour l'encodage
			mimetype = "application/force-download"

			if guessed_type:
				mimetype = guessed_type

			# response = HttpResponse(file(filepath), content_type="application/force-download") #ça ne marche avec python 3
			response = HttpResponse(wrapper, content_type=mimetype) 

			if not request.GET.get("preview"):
				response["Content-Disposition"]= "attachement; filename=%s"%(obj.media.name) #Permet de gérer le nom du fichier en téléchargement, si on utilise pas cette fonction le fichier prend le nom par défaut 'tétéchargement' pour un système de nom en français et download pour les anglofone
					
			response["X-SendFile"] = str(obj.media.name)
			return response

		else:
			raise Http404
 