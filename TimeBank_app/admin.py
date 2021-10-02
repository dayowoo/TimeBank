from django.contrib import admin
from .models import Post, Comment, Apply, Review, ReComment, Category

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(ReComment)
admin.site.register(Apply)
admin.site.register(Review)
