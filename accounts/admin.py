from django.contrib import admin
from accounts.models import Profile
from django.contrib.auth.models import User


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'nickname']


admin.site.register(Profile, ProfileAdmin)
