from django.contrib import admin
from .models import Post, MainCategory, SubCategory, Comment

admin.site.register(Post)
admin.site.register(MainCategory)
admin.site.register(SubCategory)
admin.site.register(Comment)
# admin.site.register(Relation)