from django.urls import path, re_path
from .views import login, facebook_login


app_name = "accounts"


urlpatterns = [
      re_path(r'login/$',login, name="login"),
      re_path(r'facebook-login/$', facebook_login, name="facebook_login"),
      # url(r'^logout/', auth_views.logout, {"next_page": "accounts:login"}, name="logout"),
 
    ]