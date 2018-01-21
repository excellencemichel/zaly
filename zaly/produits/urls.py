from django.urls import path, re_path

from .views import (p_home, 
					create_produit,
					update_produit,
					detail_produit,
					ProduitListView,
					ProduitDetailView,

				)


app_name = "produits"


urlpatterns = [


		path("p_home", p_home, name="p_home"),

		path("create", create_produit, name="create_produit"),
		re_path(r'^detail/(?P<object_id>\d+)-(?P<slug>[\w-]+)/$', detail_produit, name="detail_produit"),
		re_path(r'^detail/(?P<object_id>\d+)-(?P<slug>[\w-]+)/edit/$', update_produit, name="update_produit"),
		# re_path(r'^produit/(?P<object_id>\d+)-(?P<slug>[\w-]+)/edit/$',)
		re_path(r'^list/$', ProduitListView.as_view(), name="list_produit"),
		re_path(r'^(?P<pk>\d+)/$', ProduitDetailView.as_view(), name="produit_detail_view"),




]