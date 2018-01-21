from django import forms
from .models import Produit

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
		elif price >= 99.999:
			raise forms.ValidationError("Le prix ne doit pas être plus que $100.000")
		else:
			return price


class ProduitModelForm(forms.ModelForm):
	class Meta:
		model = Produit
		fields = [
			"title",
			"description",
			"price",
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

	def clean_price(self):
		price = self.cleaned_data.get("price")
		if price <= 1.000:
			raise forms.ValidationError("Le prix doit être plus $1.000")

		elif price >= 100.000:
			raise forms.ValidationError("Le prix ne doit pas depasser $100.000")

		else:
			return price