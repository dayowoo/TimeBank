from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('shop_list/', shop_list, name="shop_list"),
    path('product_new/', product_new, name="product_new"),
    path('product_create/', product_create, name="product_create"),
    path('product_detail/<int:product_id>', product_detail, name="product_detail"),

    path('product_detail/<product_id>/create_product_comment', create_product_comment, name="create_product_comment"),
    path('product_detail/<product_id>/<comment_id>/delete_product_comment', delete_product_comment, name="delete_product_comment"),

    path('product_detail/<product_id>/<comment_id>/create_product_recomment', create_product_recomment, name="create_product_recomment"),
    path('product_detail/<product_id>/<comment_id>/<recomment_id>/create_product_rerecomment', create_product_rerecomment, name="create_product_rerecomment"),
    path('product_detail/<product_id>/<comment_id>/<recomment_id>/delete_product_recomment', delete_product_recomment, name="delete_product_recomment"),

    path('product_detail/<product_id>/product_apply', product_apply, name="product_apply"),
    path('product_detail/<product_id>/<user_id>/product_choice', product_choice, name="product_choice"),
    path('product_detail/<product_id>/<user_id>/product_success', proudct_success, name="product_success"),
    path('product_detail/<product_id>/<user_id>/product_stop', product_stop, name="product_stop"),
    path('product_detail/<product_id>/<user_id>/product_success_ck', product_success_ck, name="product_success_ck")
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)