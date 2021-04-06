from django.db import models
from django.conf import settings
from TimeBank_account.models import User

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
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    service_choice = (('give','주고싶어요'), ('take','받고싶어요'))
    service = models.CharField(max_length=50, choices=service_choice)
    location = models.CharField(max_length=140)
    main_work = models.ForeignKey('MainCategory', on_delete = models.CASCADE, null=True)
    sub_work = models.ForeignKey(SubCategory, on_delete = models.CASCADE, related_name='MainCategory', null=True)
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    tok = models.PositiveIntegerField(default=0, verbose_name='거래톡')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    applicants = models.ManyToManyField(User, blank=True, related_name='applier')
    status_list = (('대기','대기'),('진행','진행'),('완료','완료'),('중단','중단'))
    status = models.CharField(max_length=50, choices=status_list, default='대기')
    respond_list = (('요청대기','요청대기'),('요청승인', '요청승인'),('요청거절','요청거절'))
    respond = models.CharField(max_length=50, choices=respond_list, default='요청대기')

    # 객체 목록 가져오기 (작성 순서대로)
    class Meta:
        ordering = ['-created_at']

    @property
    def index(self):
        return self.work_choice[:50]

    def __str__(self):
        return self.content

'''
    def usermode(self):

        if self.author == User.username:
            if self.service == "give":
                usermode = "giver"
            else:
                usermode = "taker"
        else:
            usermode = "none"
            #if self.objects.get(applicants = User.is_active):
            #    usermode = "applicant"
            #else:
            #    usermode = "none"
        
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


# 거래톡 보내기
class MessageItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="신청자")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="원글")
    status_list = (('register','신청하기'),('register_complete','신청완료'),
                    ('wait','대기중'),('complete','완료하기'),('fail','중단'))
    status = models.CharField(max_length=50, choices=status_list, default='대기중')
    # applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applier', null=True)
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

