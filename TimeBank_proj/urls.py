from django.contrib import admin
import TimeBank_account.views
import TimeBank_app.views
from django.urls import path, include
from django. conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TimeBank_app.urls')),
    path('account/', include('TimeBank_account.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)