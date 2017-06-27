from django.contrib import admin
from .models import UserProfile
# Register your models here.


class UserProfileModelAdmin(admin.ModelAdmin):
    list_display = ['user']
admin.site.register(UserProfile, UserProfileModelAdmin)