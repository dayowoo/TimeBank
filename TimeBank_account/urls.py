from django.urls import path, include
from . import views
from django. conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<str:username>', views.profile, name="profile"),
    path('profile_update_page/<str:username>', views.profile_update_page, name="profile_update_page"),
    path('profile_update/<str:username>', views.profile_update, name="profile_update"),
    path('account', views.account_history, name="account"),
    path('balance_create/<int:account_id>', views.create_account_no, name="create_account_no"),
    path('balance', views.balance, name="balance"),
    path('my_post_detail/<int:post_id>', views.my_post_detail, name="my_post_detail"),
    path('my_post_detail/<int:post_id>/success', views.success, name="success"),                                                                                     
    path('my_post_detail/<int:post_id>/stop', views.stop, name="stop"),
    path('my_register_detail/<int:post_id>', views.my_register_detail, name="my_register_detail"),
    path('my_register_detail/<int:post_id>/reg_success', views.reg_success, name="reg_success"),
    path('my_register_detail/<int:post_id>/reg_stop', views.reg_stop, name="reg_stop"),
    path('balance_test', views.balance_test, name="balance_test"),
]