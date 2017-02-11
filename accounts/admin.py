from django.contrib import admin
from accounts.models import Profile
from django.contrib.auth.models import User


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'school']
    search_fields = ['school']


admin.site.register(Profile, ProfileAdmin)
