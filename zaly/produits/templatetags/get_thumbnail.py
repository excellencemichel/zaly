from django import template

from ..models import Produit, THUMB_CHOICES

register = template.Library()


@register.filter
def get_thumbnail(obj, arg):
	"""
		obj == Produit instance
	"""
	arg = arg.lower()
	if not isinstance(obj, Produit):
		raise TypeError("This is not a valid produit model")

	choices = dict(THUMB_CHOICES)
	if not choices.get(arg):
		raise TypeError("This is not a valid type for this model.")

	try:
		"""Au cas oû"""
		return obj.thumbnail_set.filter(type=arg).first().media.url
	except:
		return None

	# return obj.thumbnail_set.filter(type=arg).first().media.url


