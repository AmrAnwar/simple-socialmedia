from django.conf.urls import url

from .views import (
    profile_detail,
    profile_list,
    CommentLikeToggle,
    FollowToggle,
    )

urlpatterns = [
    url(r'^$', profile_list, name="list"),
    url(r'^(?P<slug>[\w-]+)/follow/$', FollowToggle.as_view(), name="follow_toggle"),
    url(r'^comments/(?P<comment_id>\d+)/likes/$', CommentLikeToggle.as_view(), name="like_toggle"),
    url(r'^(?P<slug>[\w-]+)/$', profile_detail, name="detail"),
    # url(r'^(?P<slug>[\w-]+)/(?P<comment_id>\d+)/likes$', CommentLikeToggle.as_view(), name="like_toggle"),

]