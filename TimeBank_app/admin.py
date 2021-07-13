from django.contrib import admin
from .models import Post, MainCategory, SubCategory, Comment, Apply, Review

admin.site.register(Post)
admin.site.register(MainCategory)
admin.site.register(SubCategory)
admin.site.register(Comment)
admin.site.register(Apply)
admin.site.register(Review)
