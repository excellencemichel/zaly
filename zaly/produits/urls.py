from django.urls import path, re_path

from .views import (p_home,
					create_produit_simple,
					create_produit,
					update_produit,
					detail_produit,
					ProduitListView,
					ProduitDetailView,
					ProduitCreateView,
					ProduitUpdateView,
					ProduitDownloadView,

				)


app_name = "produits"


urlpatterns = [


		path("p_home", p_home, name="p_home"),

		path("create", create_produit, name="create"),
		path("ajout", create_produit_simple, name="simple_ajout"),
		re_path(r'^detail/(?P<object_id>\d+)-(?P<slug>[\w-]+)/$', detail_produit, name="detail"),
		re_path(r'^detail/(?P<object_id>\d+)-(?P<slug>[\w-]+)/edit/$', update_produit, name="update"),
		# re_path(r'^produit/(?P<object_id>\d+)-(?P<slug>[\w-]+)/edit/$',)
		path("", ProduitListView.as_view(), name="list"),
		re_path(r'^(?P<pk>\d+)/$', ProduitDetailView.as_view(), name="detail_view"),
		re_path("add", ProduitCreateView.as_view() , name="add"),
		re_path(r'^(?P<slug>[\w-]+)/$', ProduitDetailView.as_view(), name="detail_slug_view"),
		re_path(r'^detail/(?P<pk>\d+)-(?P<slug>[\w-]+)/$', ProduitDetailView.as_view(), name="detail_id_slug_view"),
		re_path(r'^(?P<pk>\d+)/edit/$', ProduitUpdateView.as_view(), name="update_view"),
		re_path(r'^(?P<slug>[\w-]+)/edit/$', ProduitUpdateView.as_view(), name="update_slug_view"),



		re_path(r'^(?P<pk>\d+)/download/$', ProduitDownloadView.as_view(), name="download_view"),
		re_path(r'^(?P<slug>[\w-]+)/download/$', ProduitDownloadView.as_view(), name="download_slug_view"),











]