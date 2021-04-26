from django.contrib import admin
import TimeBank_account.views
import TimeBank_app.views
from django.urls import path, include
from django. conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', TimeBank_app.views.index, name="index"),
    path('admin/', admin.site.urls),
    path('post/', include('TimeBank_app.urls')),
    path('account/', include('TimeBank_account.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# DEBUG
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         path('__debug__', include(debug_toolbar.urls)),
#     ]
