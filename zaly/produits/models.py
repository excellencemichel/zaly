from django.db import models

from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

# Create your models here.


class Produit(models.Model):
	title = models.CharField(max_length=250)
	slug = models.SlugField(blank=True) #L'argument blank nous permet de gérer le signal pour que si
	#slug est vide pendant la création on rempli 
	description = models.TextField()
	price = models.DecimalField(max_digits=19, decimal_places=3)
	sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)

	def __str__(self):
		return self.title




# La gestion des signaux

def produit_pre_save_receiver(sender, instance, *args, **kwargs):
	print(instance)
	print(sender)
	if not instance.slug:
		instance.slug = slugify(instance.title)



pre_save.connect(produit_pre_save_receiver, sender=Produit)
