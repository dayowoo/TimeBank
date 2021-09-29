from django.contrib import admin
from .models import User, Account, PropertyTag

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')

admin.site.register(User, UserAdmin)
admin.site.register(Account)
admin.site.register(PropertyTag)