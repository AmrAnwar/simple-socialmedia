# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from django.conf import settings
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType


# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", null=True, blank="True")

    class Meta:
        ordering = ['-timestamp']

    def children(self):
        return Comment.objects.filter(parent=self)

