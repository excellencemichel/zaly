from django.utils.text import slugify

from django import forms
from .models import Produit

PUBLISH_CHOICES = (
			("publish", "Publish"),
			("draft", "Draft"),
	)

class ProduitForm(forms.Form):
	title = forms.CharField( widget= forms.TextInput(
			attrs = {
				"class":"la class",
				"placeholder": "Le super titre",
			}
		))
	description = forms.CharField( widget = forms.Textarea(
		attrs = {
			"class": "my-custom-class",
			"placeholder": "La description",
			"some-attr": "this",
		}))
	price = forms.DecimalField()


	def clean_price(self):
		price = self.cleaned_data.get("price")

		if price <= 1.000:
			raise forms.ValidationError("Le prix doit être plus que $1.000")
		elif price >= 333:
			raise forms.ValidationError("Le prix ne doit pas être plus que $100.000")
		else:
			return price


class ProduitModelForm(forms.ModelForm):
	tags = forms.CharField(label="Related tags", required=False)
	publish = forms.ChoiceField(widget=forms.RadioSelect, choices=PUBLISH_CHOICES, required=False)
	class Meta:
		model = Produit
		fields = [
			"title",
			"description",
			"price",
			"tags",
			"publish",
			"media",
		]

		widgets = {
			"description": forms.Textarea(
					attrs={
						"placeholder": "New description",
					}
				),
			
			"title": forms.TextInput(
					attrs = {
						"placeholder":"New title",
					}
			)
		 }



	def clean(self, *args, **kwargs):
		cleaned_data = super(ProduitModelForm, self).clean(*args, **kwargs)
		# title = cleaned_data.get("title")
		# slug = slugify(title)

		# qs = Produit.objects.filter(slug=slug).exists()

		# if qs:
		# 	raise forms.ValidationError("Title is taken, new is needed. Please try again.")

		print (cleaned_data)
		return cleaned_data

	def clean_price(self):
		price = self.cleaned_data.get("price")
		if price <= 1.000:
			raise forms.ValidationError("Le prix doit être plus $1.000")

		elif price >= 100.000:
			raise forms.ValidationError("Le prix ne doit pas depasser $100.000")

		else:
			return price

	def clean_title(self):
		title = self.cleaned_data.get("title")

		if len(title) > 3:
			return title

		else:
			raise forms.ValidationError("The title must be greater than 3 characters long.")
