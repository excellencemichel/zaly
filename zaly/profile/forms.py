from datetime import date
from re import match

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _



class UserCreationForm(forms.ModelForm):

	error_messages = {
	    'duplicate_username': _("A user with that username already exist. "),
	    'duplicate_email': _("A user with that email already exist."),
	    'password_mismatch' : _("The two password fields didn'it match. "),

	    }


	username = forms.CharField(
	    						widget =forms.TextInput(attrs={"class": "form-control input-sm", "placeholder":"username"}),
    	                        )

	first_name = forms.CharField(

		                      widget =forms.TextInput(attrs={"class": "form-control input-sm", "placeholder":"Prénom"}),
    	                        
		                     )

	last_name = forms.CharField(
								widget =forms.TextInput(attrs={"class": "form-control input-sm", "placeholder":"Nom"}),
    	                       )

	email = forms.EmailField(widget = forms.EmailInput(attrs={"class": "form-control input-sm", "placeholder":"Adresse mail"}),
		                    )
	password1 = forms.CharField(
		label=_("Password"),
	    widget =forms.PasswordInput(attrs={"class": "form-control input-sm", "placeholder":"Password"}),
	    	   )
	password2 = forms.CharField(
	    	label=_("Confirmation"),
	    	widget =forms.PasswordInput(attrs={"class": "form-control input-sm", "placeholder":"Password"}),
	    	help_text=_("Enter the same password as above, for verification.")
	    	)


	date_suggession = ("2012","2010","2009","2008","2007","2006","2005","2004","2003", "2002","2001","2000","1999","1998","1997","1996","1995","1994",
		                 "1993","1992","1991","1990","1989","1988","1987","1986","1985","1984","1983","1982",
		                 "1981","1980","1979","1978","1977","1976","1975","1974","1973","1972","1971","1970","1969",
		                 "1968","1967","1966","1965","1964","1963","1962","1961","1960","1959","1958","1957","1956",
		                 "1955","1954","1953","1952","1951","1950","1949","1948","1947","1946","1945","1944","1943",
		                 "1942","1941","1940","1939","1938","1937","1936","1935","1934","1933","1932","1931","1930",)

	birth_day = forms.DateField(label=_("Anniversaire"), widget=forms.SelectDateWidget(years=date_suggession,))

	mobile = forms.CharField(label=_("Le numéro de téléphone"),
	    	               widget =forms.TextInput(attrs={"class": "form-control input-sm", "placeholder":"Tél"}),
		                   help_text=_("Vous pouvez séparez les numéro par des espace pour faciter la compréhension")
		                   )

	class Meta:
	    model = get_user_model()
	    fields = ("username", "first_name", "last_name", "email", "mobile", "birth_day",)



	def clean_username(self):

	    username = self.cleaned_data["username"]
	    try:
	    	get_user_model()._default_manager.get(username=username)
	    except get_user_model().DoesNotExist:
	    	return username

	    raise forms.ValidationError(
	    		self.error_messages['duplicate_username'],
	    		 code ='duplicate_username',
	    		 )


	def clean_email(self):
		email = self.cleaned_data["email"]
		try:
			get_user_model()._default_manager.get(email=email)
		except get_user_model().DoesNotExist:
			return email
		raise forms.ValidationError(
	    		self.error_messages['duplicate_email'],
	    		code='duplicate_email',
	    		)


	def clean_password2(self):
	    password1 = self.cleaned_data.get("password1")
	    password2 = self.cleaned_data.get("password2")

	    if password1 and password2 and password1 != password2:
	    	raise forms.ValidationError(
	    			self.error_messages['password_mismatch'],
	    			code='password_mismatch',
	    			)
	    return password2


	def clean_mobile(self):
		mobile = self.cleaned_data["mobile"]
		controle = r"^6[2-9][0-9]([ .-]?[0-9]{2}){3}$"

		if match(controle, mobile):
			return mobile
		else:
			raise forms.ValidationError(_("Votre numéro de téléphone ne correspond pas à un numéro de téléphone guinéen"))


	def save(self, commit=True):

	    user = super(UserCreationForm, self).save(commit=False)
	    user.set_password(self.cleaned_data['password2'])
	    if commit:
	    	user.save()
	    return user




class ProfileUserChangeForm(forms.ModelForm):

	password = ReadOnlyPasswordHashField(label=_("Password"),
		   help_text = _(
		   	"Raw passwords are not stored, so there is no way to see"
		   	"this user's password, but you can change the password"
		   	"using <a href=\"%(url)s\">this form</a>.") %{'url': '../password/'})


	class Meta:
		model = get_user_model()
		exclude = ()


	def __init__(self, *args, **kwargs):
		super(ProfileUserChangeForm, self).__init__(*args, **kwargs)
		f = self.fields.get('user_permissions', None)
		if f is not None:
			f.queryset = f.queryset.select_related("content_type")


	def clean_password(self):
		return self.initial["password"]





class ConnexionForm(forms.Form):
	username = forms.CharField(max_length=250)
	password = forms.CharField(widget=forms.PasswordInput)