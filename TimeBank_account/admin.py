from django.contrib import admin
from .models import User, Account

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'password')

admin.site.register(User, UserAdmin)
admin.site.register(Account)