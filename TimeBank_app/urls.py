from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('new_post/', views.create, name="new_post"),
]
