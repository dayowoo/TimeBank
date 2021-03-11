from django.contrib import admin
import TimeBank_account.views
import TimeBank_app.views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TimeBank_app.urls')),
    path('account/', include('TimeBank_account.urls')),
]
