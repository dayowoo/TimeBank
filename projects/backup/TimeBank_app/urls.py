from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
# import TimeBank_account.views

urlpatterns = [
    path('post_list/', post_list, name="post_list"),
    path('post_list_search/', post_list_search, name="post_list_search"),
    path('post_ajax/', post_ajax, name="post_ajax"),
    path('new_post/', new_post, name="new_post"),
    path('new_post_step1/', new_post_step1, name="new_post_step1"),
    path('completed_post/', completed_post, name="completed_post"),
    path('completed_post/completed_search', completed_search, name="completed_search"),
    path('completed_create/', completed_create, name="completed_create"),
    path('create/', create, name="create"),
    path('post_detail/<post_id>/update_page', update_page, name="update_page"),
    path('post_detail/<post_id>/update', update, name="update"),
    path('post_detail/<post_id>/delete/', delete, name="delete"),
    path('post_detail/<post_id>/apply', apply, name="apply"),
    path('post_detail/<post_id>/<user_id>/choice', choice, name="choice"),
    path('post_detail/<post_id>/<user_id>/success', success, name="success"),
    path('post_detail/<post_id>/<user_id>/success_ck', success_ck, name="success_ck"),
    path('post_detail/<post_id>/<user_id>/stop', stop, name="stop"),
    path('post_detail/<post_id>', post_detail, name="post_detail"),
    path('post_detail/<post_id>/create_post_comment', create_post_comment, name="create_post_comment"),
    path('post_detail/<post_id>/<comment_id>/delete_post_comment', delete_post_comment, name="delete_post_comment"),
    path('post_detail/<post_id>/<comment_id>/create_post_recomment', create_post_recomment, name="create_post_recomment"),
    path('post_detail/<post_id>/<recomment_id>/delete_post_recomment', delete_post_recomment, name="delete_post_recomment"),
    path('<post_id>/new_review/', new_review, name="new_review"),
    path('<post_id>/create_review/', create_review, name="create_review"),
    path('<post_id>/review_detail/<review_id>', review_detail, name="review_detail"),
    path('<post_id>/review_update_page/<review_id>', review_update_page, name="review_update_page"),
    path('<post_id>/review_detail/<review_id>/review_delete', review_delete, name="review_delete"),
    path('<post_id>/review_update/<review_id>', review_update, name="review_update"),
    # path(r'^post_list/(?P<post_id>\d+)/$', progress, name="progress"),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)