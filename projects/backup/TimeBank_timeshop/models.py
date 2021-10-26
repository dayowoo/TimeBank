from django.db import models
from TimeBank_proj import settings
import os
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from imagekit.models import ImageSpecField



# Create your models here.
# 거래글 등록
class Product(models.Model): 
    date = models.CharField(max_length=140, blank=True)
    location = models.CharField(max_length=140)
    category_list = (('디지털기기','디지털기기'),
     ('생활가전','생활가전'),
     ('가구/인테리어','가구/인테리어'),
     ('유아동','유아동'),
     ('스포츠/레저','스포츠/레저'),
     ('여성잡화','여성잡화'),
     ('여성의류','여성의류'),
     ('남성패션/잡화','남성패션/잡화'),
     ('게임/취미','게임/취미'),
     ('뷰티/미용','뷰티/미용'),
     ('반려동물용품','반려동물용품'),
     ('도서/티켓/음반','도서/티켓/음반'),
     ('식물','식물'),
     ('기타','기타'),
     ('삽니다','삽니다'),
     )
    category = models.CharField(max_length=100, choices=category_list, null=True)
    title = models.CharField(max_length=200, default='example', verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    tok = models.DecimalField(default=1, decimal_places=2, max_digits=5, verbose_name='거래시간')
    author = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, verbose_name='작성자')
    status_list = (('대기','대기'),('진행','진행'),('완료','완료'),('완료확정','완료확정'),('중단','중단'))
    status = models.CharField(max_length=50, choices=status_list, default='대기')
    respond_list = (('요청대기','요청대기'),('요청승인', '요청승인'),('요청거절','요청거절'))
    respond = models.CharField(max_length=50, choices=respond_list, verbose_name='승인상태', default='요청대기')
    applicants = models.ManyToManyField('self', blank = True, related_name='apply_user', through='Deal', symmetrical=False)
    seller = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, related_name='seller', verbose_name='판매자', null=True)
    buyer = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, related_name='buyer', verbose_name='구매자', null=True)
    image = models.ImageField(upload_to="images/", blank=True)


    

    # 객체 목록 가져오기 (작성 순서대로)
    class Meta:
        ordering = ['-created_at']

    # 지원자 얻기
    @property
    def get_user(self):
        return [i.from_post for i in self.to_user.all()]

    
    # 삭제시, MEDIA_ROOT파일 삭제
    def imgDelete(self, *args, **kargs):
        if self.upload_files:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.upload_files.path))
        super(Product, self).delete(*args, **kargs)


    @property
    def user_count(self):
        return len(self.get_user)



class Deal(models.Model):
    from_post = models.ForeignKey('TimeBank_timeshop.Product', related_name='deal_post', on_delete=models.CASCADE)
    to_user = models.ForeignKey('TimeBank_account.User', related_name='deal_user', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now=True)

    # 관계되는 칼럼의 중복막기
    class Meta:
        unique_together = (('from_post', 'to_user'))




# 댓글 기능
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='글', null=True)
    author = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, verbose_name='댓글작성자', related_name="shopComment_author")
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='댓글등록시간')



# 답글
class ReComment(models.Model):
    comment = models.ForeignKey(Comment, related_name="recomment", on_delete=models.CASCADE, verbose_name='댓글', null=True)
    author = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, related_name="shopRecomment_author", verbose_name='답글작성자')
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='답글등록시간')
    mention = models.CharField(max_length=50, blank=True, null=True)

