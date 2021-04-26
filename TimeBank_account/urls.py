from django.urls import path, include
from . import views
from django. conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<str:username>', views.profile, name="profile"),
    path('account', views.account_history, name="account"),
    path('balance', views.balance, name="balance"),
    path('my_post_detail/<int:post_id>', views.my_post_detail, name="my_post_detail"),
    path('my_post_detail/<int:post_id>', views.success, name="success"),
    path('my_register_detail/<int:post_id>', views.my_register_detail, name="my_register_detail"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)