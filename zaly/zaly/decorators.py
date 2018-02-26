from django.http import Http404


def ajax_required(function):
	"""
	Décorateur pour l'exigence de ajax pour une
	fonction qui veut faire un traitement ajax
	"""
	def wrap(request, *args, **kwargs):
		if not request.is_ajax():
			raise Http404
		return function(request, *args, **kwargs)
	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap