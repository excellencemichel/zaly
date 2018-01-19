from django.urls import path, re_path
from django.contrib.auth.views import (password_reset, password_reset_done,
                                      password_reset_confirm, password_reset_complete



                                      )

from .views import (
				home,
                register,
                activate,



		)

app_name = "profile"


urlpatterns = [
   
               # url(r'^home/$', home, name="home"),

                # url(r'^logout/$', logout, name="logout"),


                re_path(r'register/$', register, name="register"),

                re_path(r'activate/(?P<uidb64>[\w\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[\w]{1,20})/$', activate, name="active"),

                #url(r'^qlq/$', qlq, name="qlq"),

                # url(r'^login/$',connexion, name="login"),


                #url(r'^update/$', update_user, name="update_user"),

               # url(r'^change_password/$', change_password, name="change_password"),

                #url(r'^reset-password/$', password_reset, name="reset_password"),
                #url(r'^reset-password/done/$', password_reset_done, name="password_reset_done"),

                #url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name="password_reset_confirm"),

               # url(r'^reset-password/complete/$', password_reset_complete, name="password_reset_complete"),





]