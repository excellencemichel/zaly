from django.contrib import admin

from .models import Produit, MyProduits


class ProduitAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",),}

	list_display = ["__str__", "description", "price", "sale_price"]
	search_fields = ["title", "description"]
	list_filter = ["price", "sale_price"]
	list_editable = ["sale_price"]

	class Meta:
		model = Produit



# Register your models here.



admin.site.register(Produit, ProduitAdmin)



admin.site.register(MyProduits)

