from django.contrib import admin
from .models import Post, Comment, Apply, Review, ReComment, Category
from mptt.admin import DraggableMPTTAdmin



# 드래그앤드롭으로 트리 구조 위치 조정
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        'category_name',
    )
    # 모델당 픽셀 레벨 지정
    mptt_level_indent = 20
    # 들여쓰기할 필드 지정
    # mptt_indent_field = "some_node_field"


admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(ReComment)
admin.site.register(Apply)
admin.site.register(Review)
