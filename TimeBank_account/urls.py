from django.urls import path, include
from . import views
from django. conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('register/id_overlap_check/', views.id_overlap_check, name="id_overlap_check"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<str:username>/profile', views.profile, name="profile"),
    path('<str:username>/profile_update_page', views.profile_update_page, name="profile_update_page"),
    path('<str:username>/profile_update', views.profile_update, name="profile_update"),
    path('<str:username>/account', views.account_history, name="account"),
    path('balance_create', views.create_account_no, name="create_account_no"),
    path('<str:username>/balance', views.balance, name="balance"),
    path('<str:username>/my_review', views.my_review, name="my_review"),
    path('my_review_detail/<review_id>', views.my_review_detail, name="my_review_detail"),
    path('my_post_detail/<int:post_id>', views.my_post_detail, name="my_post_detail"),
    path('my_post_detail/<int:post_id>/success', views.success, name="success"),                                                                                     
    path('my_post_detail/<int:post_id>/stop', views.stop, name="stop"),
    path('my_register_detail/<int:post_id>', views.my_register_detail, name="my_register_detail"),
    path('my_register_detail/<int:post_id>/reg_success', views.reg_success, name="reg_success"),
    path('my_register_detail/<int:post_id>/reg_stop', views.reg_stop, name="reg_stop"),
]