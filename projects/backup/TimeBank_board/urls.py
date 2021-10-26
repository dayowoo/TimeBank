from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('board_list/', board_list, name="board_list"),
    path('board_search/', board_search, name="board_search"),
    path('board_new/', board_new, name="board_new"),
    path('board_create/', board_create, name="board_create"),
    path('board_detail/<int:board_id>', board_detail, name="board_detail"),
    path('board_detail/<int:board_id>/update_page', board_update_page, name="board_update_page"),
    path('board_detail/<int:board_id>/update', board_update, name="board_update"),
    path('board_detail/<int:board_id>/delete/', board_delete, name="board_delete"),
    path('board_detail/<board_id>/create_comment', create_comment, name="create_comment"),
    path('board_detail/<board_id>/<comment_id>/delete_comment', delete_comment, name="delete_comment"),
    path('board_detail/<board_id>/<comment_id>/update_comment', update_comment, name="update_comment"),
    path('board_detail/<board_id>/<comment_id>/create_recomment', create_recomment, name="create_recomment"),
    path('board_detail/<board_id>/<comment_id>/<recomment_id>/create_rerecomment', create_rerecomment, name="create_rerecomment"),
    path('board_detail/<board_id>/<comment_id>/<recomment_id>/delete_recomment', delete_recomment, name="delete_recomment"),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)