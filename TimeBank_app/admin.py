from django.contrib import admin
from .models import Post, MainCategory, SubCategory, MessageItem, DealRelation
# Register your models here.

admin.site.register(Post)
admin.site.register(MainCategory)
admin.site.register(SubCategory)
admin.site.register(MessageItem)
admin.site.register(DealRelation)