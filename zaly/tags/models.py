from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify




from django.db import models

from produits.models import Produit

# Create your models here.

class TagQuerySet(models.QuerySet):
	def active(self):
		return self.filter(active=True)


class TagManager(models.Manager):
	def get_queryset(self):
		return TagQuerySet(self.model, using=self._db)
	def all(self, *args, **kwargs):
		return super(TagManager, self).all(*args, **kwargs).active()


	# def active(self, *args, **kwargs):
	# 	return self.get_queryset().filter(active=True)

class Tag(models.Model):
	title = models.CharField(max_length=255, unique=True)
	slug  = models.SlugField(max_length=255, unique=True)
	produits = models.ManyToManyField(Produit, blank=True)
	active  = models.BooleanField(default=True)
    
	objects = TagManager()

	def __str__(self):
		return str(self.title)



	def get_absolute_url(self):
		#C'est remarquable, et ça foctionne seulement si le namespace est présent
		# return "/produits/%s/"%(self.slug)
		view_name_with_id = "tags:detail_view"
		view_name_with_slug = "tags:detail_slug_view"
		view_name_with_id_and_slug = "tags:detail_id_slug_view"


		# return reverse(view_name_with_id, kwargs={"id": self.id})
		# peut aussi marcher
		# return reverse(view_name_with_slug, kwargs={"slug":self.slug})
		return reverse(view_name_with_id_and_slug, kwargs={"pk":self.pk, "slug":self.slug})





def tag_pre_save_receiver(sender, instance, *args, **kwargs):
	instance.title = instance.title.lower()
	if not instance.slug:
		instance.slug = slugify(instance.title)



pre_save.connect(tag_pre_save_receiver, sender=Tag)