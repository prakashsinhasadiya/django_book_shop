from django.contrib import admin
from .models import UserProfile,BookDetail,PasswordResetTokens

class ProfileAdmin(admin.ModelAdmin):

    list_display = ['user', 'mobile','first_name','last_name','email','profile_image']
    search_fields = ['user__username', 'mobile']


class BookDetailAdmin(admin.ModelAdmin):
    
    list_display = ['book_name','slug','auther_name','book_price','book_image','book_file']
    search_fields = ['user__bookname', 'user','book_name']

class PasswordResetTokensAdmin(admin.ModelAdmin):
    list_display = ['user', 'token']

admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(BookDetail, BookDetailAdmin)
admin.site.register(PasswordResetTokens, PasswordResetTokensAdmin)