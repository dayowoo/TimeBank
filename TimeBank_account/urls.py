from django.urls import path, include
from . import views
from django. conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<str:userid>', views.profile, name="profile"),
    path('account', views.account_history, name="account"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
