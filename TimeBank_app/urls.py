from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
# import TimeBank_account.views

urlpatterns = [
    path('post_list/', post_list, name="post_list"),
    path('new_post/', new_post, name="new_post"),
    path('create/', create, name="create"),
    path('post_detail/<post_id>/apply', apply, name="apply"),
    path('post_detail/<post_id>', post_detail, name="post_detail"),
    path('post_detail/<post_id>/create_comment', create_comment, name="create_comment")
    # path(r'^post_list/(?P<post_id>\d+)/$', progress, name="progress"),
    # path('progress_ajax/', progress_ajax, name="progress_ajax"),
    # path('post_ajax/', post_ajax, name="post_ajax"),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  