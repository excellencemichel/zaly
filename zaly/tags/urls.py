from django.urls import path, re_path

from .views import (
                        TagDetailView,
                        TagListView,
                )


app_name = "tags"


urlpatterns = [


        path("", TagListView.as_view(), name="list"),
        re_path(r'^(?P<pk>\d+)/$', TagDetailView.as_view(), name="detail_view"),
        re_path(r'^(?P<slug>[\w-]+)/$', TagDetailView.as_view(), name="detail_slug_view"),
        re_path(r'^detail/(?P<pk>\d+)-(?P<slug>[\w-]+)/$', TagDetailView.as_view(), name="detail_id_slug_view"),











]