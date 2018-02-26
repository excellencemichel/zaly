from django.urls import path, re_path

from .views import (
					SellerAccountDashboard,
				)


app_name = "sellers"


urlpatterns = [

    path("", SellerAccountDashboard.as_view(), name="dashboard"),


]