from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TimeBank_app.urls')),
    path('register/', include('TimeBank_account.urls')),
    path('login/', include('TimeBank_account.urls')),
]
