from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.db import models


# Create your models here.
def download_media_location(instance, filename):
	return "%s/%s" %(instance.id, filename)



class Produit(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers_produits")
	media = models.FileField(blank=True, null=True,
	 upload_to=download_media_location,
	 storage = FileSystemStorage(location=settings.PROTECTED_ROOT)

	 )
	title = models.CharField(max_length=250)
	slug = models.SlugField(blank=True, unique=True) #L'argument blank nous permet de gérer le signal pour que si
	#slug est vide pendant la création on rempli 
	description = models.TextField()
	price = models.DecimalField(max_digits=19, decimal_places=3)
	sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)

	def __str__(self):
		return self.title



	def get_absolute_url(self):
		#C'est remarquable, et ça foctionne seulement si le namespace est présent
		# return "/produits/%s/"%(self.slug)
		view_name_with_id = "produits:detail_view"
		view_name_with_slug = "produits:detail_slug_view"
		view_name_with_id_and_slug = "produits:detail_id_slug_view"


		# return reverse(view_name_with_id, kwargs={"id": self.id})
		# peut aussi marcher
		# return reverse(view_name_with_slug, kwargs={"slug":self.slug})
		return reverse(view_name_with_id_and_slug, args={self.id,self.slug})


	def get_download(self):
		view_name = "produits:download_slug_view"
		url = reverse(view_name, kwargs={"slug":self.slug})
		return url






#Creation d'une fonction pour gérer le slug avec un signal
def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)

	if new_slug is not None:
		slug = new_slug

	qs = Produit.objects.filter(slug=slug)
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)

	return slug

# La gestion des signaux

def produit_pre_save_receiver(sender, instance, *args, **kwargs):
	print(instance)
	print(sender)
	if not instance.slug:
		instance.slug = create_slug(instance)



pre_save.connect(produit_pre_save_receiver, sender=Produit)








class MyProduits(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	produits = models.ManyToManyField(Produit, blank=True)



	def __str__(self):
		return "%s" %(self.produits.count())


	class Meta:
		verbose_name = "My Produits"
		verbose_name_plural = "My Produits"