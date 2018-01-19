from django.contrib.auth.models import (
    AbstractBaseUser, UserManager, PermissionsMixin
	)

from django.core.mail import send_mail
from django.db import models
from django.utils import timezone, six
from django.utils.translation import ugettext_lazy as _

from .validators import UnicodeUsernameValidator, ASCIIUsernameValidator


# Create your models here.

# def uplaod_location(instance, filename):
# 	extension = filename.split(".")[-1]
# 	return "profile_pictures/%s.%s" %(instance.id, extension)


def uplaod_location(instance, filename):
	extension = filename.split(".")[-1]
	jour = strftime("%a")
	temps = strftime("%d-%m-%Y-%H-%M-%S")
	pseudo = randrange(-1000000,1000000)
	print(extension)
	return "{}/{}_{}.{}".format(jour, temps, pseudo, extension)

class AbstractProfileUser(AbstractBaseUser, PermissionsMixin):

	username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

	username = models.CharField(
		_("username"),
		max_length=250,
		unique=True,
		#help_text=_("Required 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
		validators = [username_validator],
		error_messages={
		"unique": _("A user with that username already exists."),
		},
		)

	first_name = models.CharField(_("first name"), max_length=250, blank=True)
	last_name = models.CharField(_("last name"), max_length=250, blank=True)

	email = models.EmailField(_("email address"), blank=True)
	is_staff = models.BooleanField(_("staff status"),
		                      default=False,
		                      help_text=_("Designates whether the user can log into this admin site."),
		                      )
	is_active = models.BooleanField(
					_("active"),
					default=True,
					help_text=_(
						"Designates whether this user should be treaded as active."
						"Unselect this instead of deleting accounts."
						),
		)


	date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

	birth_day = models.DateField(blank=True,null=True)
	mobile = models.CharField(max_length=20)

	image_profile = models.FileField(upload_to=uplaod_location, blank=True)

	objects = UserManager()


	EMAIL_FIELD ="email"
	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = ["email"]


	class Meta:
		verbose_name = _("user")
		verbose_name_plural = _("users")
		abstract = True


	def clean(self):
		super(AbstractProfileUser, self).clean()
		self.email = self.__class__.objects.normalize_email(self.email)



	def get_full_name(self):
		full_name = "%s %s" %(self.first_name, self.last_name)
		return full_name


	def get_short_name(self):
		return self.first_name


	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], **kwargs)






class ProfileUser(AbstractProfileUser):
	class Meta(AbstractProfileUser.Meta):
		swappable = "AUTH_USER_MODEL"






