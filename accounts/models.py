from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.urls import reverse


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    interests = models.CharField(max_length=100, default="")
    slug = models.SlugField(unique=True, null=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                       related_name="followers")

    def get_absolute_url(self):
        return reverse("accounts:detail", kwargs={"slug": self.slug})

    def get_follow_instances(self):
        return self.followers.all()

    def get_follow_url(self):
        return reverse("accounts:follow_toggle", kwargs={"slug": self.slug})

    @property
    def get_instance_centent_type(self):
        return ContentType.objects.get_for_model(self.__class__)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.user.username)
    if new_slug is not None:
        slug = new_slug
    qs = UserProfile.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug)
    return slug


def create_profile(sender, instance, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=instance)
        user_profile.slug = create_slug(user_profile)
        user_profile.save()
        print (user_profile.slug)


post_save.connect(create_profile, sender=User)
