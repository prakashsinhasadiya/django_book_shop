from django.contrib import admin
from .models import UserProfile

class ProfileAdmin(admin.ModelAdmin):

    list_display = ['user', 'mobile','first_name','last_name','email','profile_image']
    search_fields = ['user__username', 'mobile']

admin.site.register(UserProfile, ProfileAdmin)
