from django.conf.urls import url

from .views import (
    profile_detail,
    profile_list
    )

urlpatterns = [
    url(r'^$',profile_list, name="list"),
    url(r'^(?P<slug>[\w-]+)/$', profile_detail, name="detail"),
]