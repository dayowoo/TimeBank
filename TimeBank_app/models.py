from django.db import models
from django.conf import settings
# from TimeBank_account.models import User
import TimeBank_account.models
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from TimeBank_proj import settings



class MainCategory(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete = models.CASCADE, null=True)
    name  = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


# 거래글 등록
class Post(models.Model): 
    date = models.CharField(max_length=140, blank=True)
    start_time = models.CharField(max_length=140, blank=True)
    end_time = models.CharField(max_length=140, blank=True)
    service_choice = (('주고싶어요','주고싶어요'),('받고싶어요','받고싶어요'))
    service = models.CharField(max_length=50, choices=service_choice)
    location = models.CharField(max_length=140)
    main_list = (('청소 / 심부름','청소 / 심부름'),
     ('몸 가꾸기 / 치장하기','몸 가꾸기 / 치장하기'),
     ('수선/ 수리','수선/ 수리'),
     ('상담','상담'),
     ('이동','이동'),
     ('먹기','먹기'),
     ('교육 / 여가생활','교육 / 여가생활'),
     ('정서지지','정서지지'),
     ('돌봄','돌봄'),
     ('식물 가꾸기','식물 가꾸기'),
     ('모임 장소 대여','모임 장소 대여'),
     ('의사소통','의사소통'),
     ('건강관리','건강관리'),
     ('기타','기타'),
     )
    mainwork = models.CharField(max_length=100, choices=main_list, null=True)
    subwork = models.CharField(max_length=200, verbose_name='세부 목록', default='')
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    tok = models.DecimalField(default=1, decimal_places=2, max_digits=5, verbose_name='거래시간')
    author = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, verbose_name='작성자')
    status_list = (('대기','대기'),('진행','진행'),('완료','완료'),('완료확정','완료확정'),('중단','중단'))
    status = models.CharField(max_length=50, choices=status_list, default='대기')
    respond_list = (('요청대기','요청대기'),('요청승인', '요청승인'),('요청거절','요청거절'))
    respond = models.CharField(max_length=50, choices=respond_list, verbose_name='승인상태', default='요청대기')
    # applicants = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, related_name='applicants', verbose_name='지원자', null=True)
    # symmetrical 이 true로 되어 있다면, 한명이 follow 하면 바로 맞팔이 되어버림
    applicants = models.ManyToManyField('self', blank = True, related_name='apply_user', through='Apply', symmetrical=False)
    giver = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, related_name='give_user', verbose_name='주는사람', null=True)
    taker = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, related_name='take_user', verbose_name='받는사람', null=True)
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
        super(Post, self).delete(*args, **kargs)


    @property
    def user_count(self):
        return len(self.get_user)



class Apply(models.Model):
    from_post = models.ForeignKey('TimeBank_app.Post', related_name='apply_post', on_delete=models.CASCADE)
    to_user = models.ForeignKey('TimeBank_account.User', related_name='apply_user', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now=True)

    # 관계되는 칼럼의 중복막기
    class Meta:
        unique_together = (('from_post', 'to_user'))




# 댓글 기능
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='글', null=True)
    author = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, verbose_name='댓글작성자')
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='댓글등록시간')



# 답글
class ReComment(models.Model):
    comment = models.ForeignKey(Comment, related_name="recomments", on_delete=models.CASCADE, verbose_name='댓글', null=True)
    author = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, verbose_name='답글작성자')
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='답글등록시간')

    

# 리뷰
class Review(models.Model):
    author = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, related_name="author", verbose_name='후기작성자')
    partner = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, related_name="partner", verbose_name='거래자')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='리뷰등록시간')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='글', null=True)
    content = models.TextField(blank=True)
    hour = models.DecimalField(default=0, decimal_places=2, max_digits=5, verbose_name='실거래시간')
    star = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True)
    image = models.ImageField(upload_to="images/", blank=True)

    # 삭제시, MEDIA_ROOT파일 삭제
    def imgDelete(self, *args, **kargs):
        if self.upload_files:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.upload_files.path))
        super(Review, self).delete(*args, **kargs)







'''
# 거래글 등록
class Post(models.Model): 
    date = models.CharField(max_length=140)
    start_time = models.CharField(max_length=140)
    service_choice = (('주고싶어요','주고싶어요'), ('받고싶어요','받고싶어요'))
    service = models.CharField(max_length=50, choices=service_choice)
    location = models.CharField(max_length=140)
    #main_work = models.ForeignKey('MainCategory', on_delete = models.CASCADE, null=True)
    #sub_work = models.ForeignKey(SubCategory, on_delete = models.CASCADE, related_name='MainCategory', null=True)
    main_work = models.CharField(max_length=140)
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    tok = models.PositiveIntegerField(default=0, verbose_name='거래톡')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    # = like_user_set
    applicants = models.ManyToManyField(User, blank=True, related_name='applier', through="MessageItem")
    status_list = (('대기','대기'),('진행','진행'),('완료','완료'),('중단','중단'))
    status = models.CharField(max_length=50, choices=status_list, default='대기')
    respond_list = (('요청대기','요청대기'),('요청승인', '요청승인'),('요청거절','요청거절'))
    respond = models.CharField(max_length=50, choices=respond_list, verbose_name='승인상태', default='요청대기')
    #giver = models.CharField(max_length=50, null=True)
    #taker = models.CharField(max_length=50, null=True)


    # 객체 목록 가져오기 (작성 순서대로)
    class Meta:
        ordering = ['-created_at']

    @property
    def index(self):
        return self.work_choice[:50]

    def __str__(self):
        return self.content

    # 신청자 목록
    @property
    def send_msg(self):
        return self.applicants.username()

    # 신청자 수
    @property
    def send_count(self):
        return self.applicants.count()


    def usermode(self):

        if self.status == "wait":
            if self.author == User.username:
                if self.service == "give":  # 주고싶어요
                    usermode = "giver"  # 봉사자
                else:
                    usermode = "taker"  # 수혜자
            else:       # 다른 사람 글
                if self.objects.get(applicants = User.is_active):
                    usermode = "applicant"
                else:
                    usermode = "none"

        elif self.status == "progress":
            if self.taker == User.username:
                usermode = "taker"
            elif self.giver == User.username:
                usermode = "giver"
            else:
                usermode = "none"

        else:
            usermode = "none"
        
        return usermode

    def btn_msg(self):

        if self.status == "대기":
            if self.usermode == "applicant":
                btn_msg = "신청 완료"
            elif self.usermode =="none":
                btn_msg = "신청하기"
            else:
                btn_msg = "시험"
        elif self.status == "진행":
            if self.usermode == "taker":
                btn_msg = "완료하기"
            else:
                btn_msg = "진행중"
        elif self.status == "완료":
            btn_msg = "완료"
        else:
            btn_msg = "중단"

        return btn_msg

'''

'''
# 거래톡 보내기
class MessageItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="신청자")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="원글")
    status_list = (('register','신청하기'),('register_complete','신청완료'),
                    ('wait','대기중'),('complete','완료하기'),('fail','중단'))
    status = models.CharField(max_length=50, choices=status_list, default='대기중')
    created_at = models.DateTimeField(auto_now_add=True)
    message_list = models.PositiveSmallIntegerField(null=True, default=0)

    class Meta:
        verbose_name = '메세지함'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']


    def respond_msg(self):
        if self.post.respond == '요청승인':
            return self.message_list + 1
        elif self.post.repond == '요청거절':
            return self.message_list
        else:
            return self.message_list


    def __str__(self):
        return self.post.content
'''

'''
class DealRelation(models.Model):
    from_post = models.ForeignKey(Post, related_name='신청글', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='지원자', on_delete=models.CASCADE)
    create_at = models.DateField(auto_now_add=True)
'''    
