from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# 사용자 정보
class User(models.Model):
    #object = UserManager()
    userid = models.CharField(max_length=64, verbose_name='사용자ID')
    email = models.EmailField(max_length=128, verbose_name='E-mail')
    username = models.CharField(max_length=64, verbose_name='이름')
    password = models.CharField(max_length=64, verbose_name='비밀번호')
    contact = models.CharField(max_length=150, verbose_name='연락처')
    birth = models.CharField(max_length=150, verbose_name='생년월일')
    user_age = models.CharField(max_length=50, verbose_name='연령대')
    gender = models.CharField(max_length=10, verbose_name='성별')

    registered_dtn = models.DateField(auto_now_add=True, verbose_name='가입일자')
    # media 폴더 내 'images'파일 저장
    image = models.ImageField(upload_to="images/", blank=True)

    # 문자열 반환(user_id문자열 반환)
    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'TimeBank_user'


# 계좌정보
class Account(models.Model):
    state_list = (
        ('deal','거래진행중'), ('request','요청진행중'),
        ('complete', '거래완료'), ('inquire', '요청보내기')
        )
    state_type = models.CharField(max_length=10, choices=state_list, verbose_name='요청상태')
    # account_no = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # PositiveIntegerField : 0 또는 양수의 값
    time_balance = models.PositiveIntegerField(default=0, verbose_name='시간계좌')
    transfer_balance = models.IntegerField(default=0, verbose_name='시간거래활동')
    bank = models.CharField(max_length=10)
    account_type_list = (
        ('give','주고싶어요'),
        ('take','받고싶어요')
        )
    account_type = models.CharField(max_length=10, choices=account_type_list)