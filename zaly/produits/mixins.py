from django.http import Http404
from zaly.mixins import LoginRequiredMixin


class ProduitManagerMixin(LoginRequiredMixin,object):


	def get_object(self, *args, **kwargs):
		user = self.request.user

		obj = super(ProduitManagerMixin, self).get_object(*args, **kwargs)

		try:
			obj.user == user
		except:
			raise Http404

		try:
			user in obj.managers.all()
		except:
			raise Http404
