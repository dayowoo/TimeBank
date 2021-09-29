from django.db import models
from django.conf import settings
from django.db.models.fields import related



# 게시판 글 등록
class Board(models.Model): 
    category_choice = (('후기','후기'),('자유글','자유글'))
    category = models.CharField(max_length=50, choices=category_choice)
    title = models.CharField(max_length=200, default='example', verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    author = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, verbose_name='작성자')
    image = models.ImageField(upload_to="images/", blank=True)

    # 객체 목록 가져오기 (작성 순서대로)
    class Meta:
        ordering = ['-created_at']



# 댓글 기능
class Comment(models.Model):
    post = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name='글', null=True)
    author = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, verbose_name='댓글작성자', related_name="comment_author")
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='댓글등록시간')



# 답글
class ReComment(models.Model):
    comment = models.ForeignKey(Comment, related_name="recomment", on_delete=models.CASCADE, verbose_name='댓글', null=True)
    author = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, verbose_name='답글작성자', related_name="recomment_author")
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='답글등록시간')
    mention = models.CharField(max_length=50, blank=True, null=True)

