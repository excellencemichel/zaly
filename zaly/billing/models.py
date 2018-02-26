
from django.conf import settings

from django.db import models


#Local
from produits.models import Produit

# Create your models here.




class Transaction(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=100, decimal_places=3, default=77)

	timestamp = models.DateTimeField(auto_now_add=True, auto_now = False)
	success =  models.BooleanField(default=True)

	#transaction_id_payement_system= Braintree/Stripe
	#payment_method =
	#last_four =


	def __str__(self):
		return "%s"%(self.id)