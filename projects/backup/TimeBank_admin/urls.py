from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)