from django.urls import path, re_path

from .views import (
					CheckoutTestView,
					CheckoutAjaxView,
				)


app_name = "checkout"


urlpatterns = [

    path("test", CheckoutTestView.as_view(), name="test"),
    path("checkout", CheckoutAjaxView.as_view(), name="checkout"),

	
	

]