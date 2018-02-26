from django.contrib import admin

from .models import Tag

# Register your models here.


class TagAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",),}



admin.site.register(Tag, TagAdmin)
