from django.contrib import admin
from .models import Board, Comment, ReComment

admin.site.register(Board)
admin.site.register(Comment)
admin.site.register(ReComment)