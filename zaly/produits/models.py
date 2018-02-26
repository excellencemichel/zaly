
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.db import models


PUBLISH_CHOICES = (
			("publish", "Publish"),
			("draft", "Draft"),
	)

# Create your models here.
def download_media_location(instance, filename):
	return "%s/%s" %(instance.slug, filename)



class Produit(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers_produits", blank=True)
	media = models.ImageField(blank=True, null=True,
	 upload_to=download_media_location,
	 storage = FileSystemStorage(location=settings.PROTECTED_ROOT)

	 )
	title = models.CharField(max_length=250)
	slug = models.SlugField(blank=True, unique=True) #L'argument blank nous permet de gérer le signal pour que si
	#slug est vide pendant la création on rempli 
	description = models.TextField()
	price = models.DecimalField(max_digits=19, decimal_places=3, default=77)
	sale_active = models.BooleanField(default=False)
	sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)

	publish = models.CharField(max_length=255, choices=PUBLISH_CHOICES)	

	def __str__(self):
		return self.title



	def get_absolute_url(self):
		#C'est remarquable, et ça foctionne seulement si le namespace est présent
		# return "/produits/%s/"%(self.slug)
		view_name_with_id = "produits:detail_id_view"
		view_name_with_slug = "produits:detail_slug_view"
		view_name_with_id_and_slug = "produits:detail"


		# return reverse(view_name_with_id, kwargs={"id": self.id})
		# peut aussi marcher
		# return reverse(view_name_with_slug, kwargs={"slug":self.slug})
		return reverse(view_name_with_id_and_slug, kwargs={"pk":self.pk , "slug":self.slug})

	# @property
	def get_download(self):
		view_name = "produits:download"
		url = reverse(view_name, kwargs={"pk":self.pk, "slug":self.slug})
		return url

	@property
	def get_price(self):
		if self.sale_price and self.sale_active:
			return self.sale_price
		return self.price






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
	# print(instance)
	# print(sender)
	if not instance.slug:
		instance.slug = create_slug(instance)



pre_save.connect(produit_pre_save_receiver, sender=Produit)





def thumbnail_location(instance, filename):
	return "%s/%s" %(instance.produit.slug, filename)

THUMB_CHOICES = (
			("hd", "HD"),
			("sd", "SD"),
			("micro", "Micro"),
	)

class Thumbnail(models.Model):
	# user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
	type = models.CharField(max_length=20, choices=THUMB_CHOICES, default="hd")
	height = models.CharField(max_length=20, blank=True, null=True)
	width = models.CharField(max_length=20, blank=True, null=True)
	media = models.ImageField(
						  width_field = "width",
						  height_field = "height",
		                  blank=True, null=True,
	 			     	  upload_to=thumbnail_location
	                     )


	def __str__(self):
		return self.type

import os
import shutil
from PIL import Image 
import random
from django.core.files import File 


def create_new_thumb(media_path, instance, owner_slug, max_height, max_width):
	filename = os.path.basename(media_path)
	thumb = Image.open(media_path)

	size = (max_height, max_width)

	thumb.thumbnail(size, Image.ANTIALIAS)
	temp_loc = "%s/%s/tmp" %(settings.MEDIA_ROOT, owner_slug)

	if not os.path.exists(temp_loc):
		os.makedirs(temp_loc)

	temp_file_path = os.path.join(temp_loc, filename)
	if os.path.exists(temp_file_path):
		temp_path = os.path.join(temp_loc, "%s" %(random.random()))
		os.makedirs(temp_path)
		temp_file_path = os.path.join(temp_path, filename)


	temp_image = open(temp_file_path, "wb")
	thumb.save(temp_image)
	thumb_data = open(temp_file_path, "rb")

	thumb_file = File(thumb_data)
	instance.media.save(filename, thumb_file)
	shutil.rmtree(temp_loc, ignore_errors=True)

	return True

def produit_post_save_receiver(sender, instance, created, *args, **kwargs):
	if instance.media:
		hd, hd_created = Thumbnail.objects.get_or_create(produit=instance, type="hd")
		sd ,sd_created = Thumbnail.objects.get_or_create(produit=instance, type="sd")
		micro, micro_created = Thumbnail.objects.get_or_create(produit=instance, type="micro")


		hd_max = (500, 500)
		sd_max = (350, 350)
		micro_max = (150, 150)

		media_path = instance.media.path
		owner_slug = instance.slug
		if hd_created:
			create_new_thumb(media_path, hd, owner_slug, hd_max[0], hd_max[1])

		if sd_created:
			create_new_thumb(media_path, sd, owner_slug, sd_max[0], sd_max[1])



		if micro_created:
			create_new_thumb(media_path, micro, owner_slug, micro_max[0], micro_max[1])


post_save.connect(produit_post_save_receiver, sender=Produit)



class MyProduits(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	produits = models.ManyToManyField(Produit)



	def __str__(self):
		return "%s" %(self.produits.count())


	class Meta:
		verbose_name = "My Produits"
		verbose_name_plural = "My Produits"
		