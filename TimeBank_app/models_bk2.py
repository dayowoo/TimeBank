from django.db import models
from django.conf import settings
# from TimeBank_account.models import User, Account
import TimeBank_account.models

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
    date = models.CharField(max_length=140)
    start_time = models.CharField(max_length=140)
    end_time = models.CharField(max_length=140)
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
    tok = models.IntegerField(default=1, verbose_name='거래톡')
    author = models.ForeignKey('TimeBank_account.User', on_delete=models.CASCADE, verbose_name='작성자')
    status_list = (('대기','대기'),('진행','진행'),('완료','완료'),('중단','중단'))
    status = models.CharField(max_length=50, choices=status_list, default='대기')
    respond_list = (('요청대기','요청대기'),('요청승인', '요청승인'),('요청거절','요청거절'))
    respond = models.CharField(max_length=50, choices=respond_list, verbose_name='승인상태', default='요청대기')
    applicants = models.CharField(max_length=140, verbose_name='신청자', null=True)
    giver = models.CharField(max_length=140, verbose_name='주는사람', null=True)
    taker = models.CharField(max_length=140, verbose_name='받는사람', null=True)
    account = models.ForeignKey('TimeBank_account.Account', related_name='Post', null=True, on_delete=models.CASCADE, verbose_name='계좌')
    account_no_to = models.CharField(max_length=20, verbose_name='받는사람 계좌번호')
    account_no_from = models.CharField(max_length=20, verbose_name='주는사람 계좌번호')
    # apply_users = models.ManyToManyField(User, related_name='apply_posts', verbose_name='신청자')

    # 객체 목록 가져오기 (작성 순서대로)
    class Meta:
        ordering = ['-created_at']

    @property
    def index(self):
        return self.work_choice[:50]

    def __str__(self):
        return self.content



'''
# 거래글 등록
class Post(models.Model): 
    date = models.CharField(max_length=140)
    start_time = models.CharField(max_length=140)
    end_time = models.CharField(max_length=140)
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

'''
class Relation(models.Model):
    from_user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='follower_user', on_delete=models.CASCADE)
    create_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} -> {}".format(self.from_user, self.to_user)
    class Meta:
        unique_together = (('from_user', 'to_user'))
'''