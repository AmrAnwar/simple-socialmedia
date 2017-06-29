# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
from accounts.models import UserProfile


# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", null=True, blank="True")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                   related_name="comment_likes")

    class Meta:
        ordering = ['-timestamp']

    def children(self):
        return Comment.objects.filter(parent=self)

    def get_like_url(self):
        return reverse("accounts:like_toggle", kwargs={"comment_id": self.id})

    def get_like_instances(self):
        return self.likes.all()

    def get_user_object(self):
        return get_object_or_404(UserProfile, user=self.user)

    def get_image_url(self):
        user_ = get_object_or_404(UserProfile, user=self.user)
        return user_.image.url
