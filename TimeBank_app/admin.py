from django.contrib import admin
from .models import Post, MainCategory, SubCategory
# Register your models here.

admin.site.register(Post)
admin.site.register(MainCategory)
admin.site.register(SubCategory)