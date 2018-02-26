from django.urls import path, re_path

from .views import (
					DashboardView,
				)


app_name = "dashboard"


urlpatterns = [

    path("", DashboardView.as_view(), name="dashboard"),


]