from django.conf.urls import url

from .views import (
    profile_detail,
    main_page,
    CommentLikeToggle,
    FollowToggle,
    search,
    profile_edit,
    )

urlpatterns = [
    url(r'^$', main_page, name="list"),
    url(r'^search/', search, name="search"),
    url(r'^comments/(?P<comment_id>\d+)/likes/$', CommentLikeToggle.as_view(), name="like_toggle"),
    url(r'^(?P<slug>[\w-]+)/follow/$', FollowToggle.as_view(), name="follow_toggle"),
    url(r'^(?P<slug>[\w-]+)/edit/$', profile_edit, name="edit"),
    url(r'^(?P<slug>[\w-]+)/', profile_detail, name="detail"),
    # url(r'^(?P<slug>[\w-]+)/(?P<comment_id>\d+)/likes$', CommentLikeToggle.as_view(), name="like_toggle"),

]