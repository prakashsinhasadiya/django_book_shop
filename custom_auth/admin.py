from django.contrib import admin
from .models import UserProfile,BookDetail

class ProfileAdmin(admin.ModelAdmin):

    list_display = ['user', 'mobile','first_name','last_name','email','profile_image']
    search_fields = ['user__username', 'mobile']


class BookDetailAdmin(admin.ModelAdmin):
    
    list_displays = ['user','book_name','auther_name','book_price','book_image','book_file']
    search_fields = ['user__bookname', 'user','book_name']


admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(BookDetail, BookDetailAdmin)