from django.conf.urls import url

from .views import (
    profile_detail,
    profile_list,
    CommentLikeToggle,
    )

urlpatterns = [
    url(r'^$',profile_list, name="list"),
    url(r'(?P<comment_id>\d+)/likes$', CommentLikeToggle.as_view(), name="like_toggle"),
    # url(r'^(?P<slug>[\w-]+)/(?P<comment_id>\d+)/likes$', CommentLikeToggle.as_view(), name="like_toggle"),
    url(r'^(?P<slug>[\w-]+)/$', profile_detail, name="detail"),

]