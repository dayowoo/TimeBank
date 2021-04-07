from django.urls import path, include
from . import views
import TimeBank_account.views

urlpatterns = [
    path('post_list/', views.post_list, name="post_list"),
    path('new_post/', views.new_post, name="new_post"),
    #path('post_list/', views.create_message, name="create_message"),
    #path('post_list_tmp2/', views.test, name="test")
]
