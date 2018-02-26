from django.contrib import admin

from .models import ( 
			Produit,
			 MyProduits,
			 Thumbnail,
			 )


class ThumbnailInline(admin.TabularInline):
	model = Thumbnail

class ProduitAdmin(admin.ModelAdmin):
	inlines = [ThumbnailInline]
	prepopulated_fields = {"slug": ("title",),}

	list_display = ["__str__", "description", "price", "sale_price", "pk"]
	search_fields = ["title", "description"]
	list_filter = ["price", "sale_price"]
	list_editable = ["sale_price"]

	class Meta:
		model = Produit



# Register your models here.



admin.site.register(Produit, ProduitAdmin)

admin.site.register(Thumbnail) #On a dejà donner à ThumbailInline de gérer

admin.site.register(MyProduits)

