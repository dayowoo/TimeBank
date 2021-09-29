from django.contrib import admin
from .models import Product, Deal, Comment, ReComment

admin.site.register(Product)
admin.site.register(Deal)
admin.site.register(Comment)
admin.site.register(ReComment)