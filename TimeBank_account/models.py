from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
class User(models.Model):
    object = UserManager()
    user_id = models.CharField(max_length=64, verbose_name='사용자ID')
    email = models.CharField(max_length=150, verbose_name='E-mail')
    username = models.CharField(max_length=64, verbose_name='사용자명')
    password = models.CharField(max_length=64, verbose_name='비밀번호')
    contact = models.CharField(max_length=150, verbose_name='연락처')
    birth = models.CharField(max_length=150, verbose_name='생년월일')
    user_age = models.CharField(max_length=50, verbose_name='연령대')
    gender = models.CharField(max_length=10, verbose_name='성별')

    registered_dtn = models.DateField(auto_now_add=True, verbose_name='가입일자')
    # media 폴더 내 'images'파일 저장
    image = models.ImageField(upload_to="images/", blank=True)

    # 문자열 반환(username문자열 반환)
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'TimeBank_user'