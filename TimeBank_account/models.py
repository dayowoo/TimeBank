from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator



class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
       
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)



# 사용자 모델
class User(AbstractUser):
    username = models.CharField(max_length=64, verbose_name='사용자ID', unique=True)
    email = models.EmailField(max_length=128, verbose_name='E-mail')
    name = models.CharField(max_length=64, verbose_name='이름')
    password = models.CharField(max_length=100, verbose_name='비밀번호')
    contact = models.CharField(max_length=150, verbose_name='연락처')
    contactCk = models.BooleanField(default=True, null=True)
    birth = models.CharField(max_length=150, verbose_name='생년월일')
    user_age = models.CharField(max_length=50, verbose_name='연령대')
    gender_choice = [('여성','여성'),('남성','남성'),('기타','기타')]
    gender = models.CharField(max_length=2, choices=gender_choice, verbose_name='성별')
    balance = models.DecimalField(decimal_places=2, max_digits=5,verbose_name='잔액', default=0)
    registered_dtn = models.DateField(auto_now_add=True, verbose_name='가입일자')
    # media 폴더 내 'images'파일 저장
    image = models.ImageField(upload_to="images/", blank=True)
    about = models.TextField(verbose_name="소개말", blank=True)
    # apply_posts = models.ManyToManyField("Post", related_name='apply_users', verbose_name='신청글')
    object = CustomUserManager()
    user_mode = [('코디네이터','코디네이터'),('사용자','사용자')]
    mode = models.CharField(max_length=60, choices=user_mode, verbose_name='유저등급', default='사용자', null=True)
    star = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, verbose_name='평균평점')

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']

    # 문자열 반환(user_id문자열 반환)
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'TimeBank_user'





# 계좌 
class Account(models.Model):
    # on_delete=models.DO_NOTHING
    post = models.ForeignKey('TimeBank_app.Post', on_delete=CASCADE, null=True, related_name='post', verbose_name='거래글')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='거래일자')
    giver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='giver', verbose_name='주는사람', null=True)
    taker = models.ForeignKey('User', on_delete=models.CASCADE, related_name='taker', verbose_name='받는사람', null=True)
    mainwork = models.CharField(max_length=100, default='', null=False)
    subwork = models.CharField(max_length=100, default='', null=False)
    tok = models.DecimalField(default=0, decimal_places=2, max_digits=5, verbose_name='거래금액')
    giver_balance = models.DecimalField(default=0, decimal_places=2, max_digits=5, verbose_name='주는사람 잔액')
    taker_balance = models.DecimalField(default=0, decimal_places=2, max_digits=5, verbose_name='받는사람 잔액')








'''
# 계좌 모델
class Account(models.Model):
    account_no = models.CharField(max_length=20, verbose_name='계좌번호')
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0, verbose_name='잔액')

    @classmethod
    def create(cls, user):
        account = cls(user=user)
        account.account_no = str(user) + '-' + user.birth
        return account



    
    def update(self):
        
        # balance 
        balance = self.user.balance

        if self.user == self.giver:
            balance = balance + self.post.tok    
        elif self.user == self.taker:
            balance = balance - self.post.tok

        self.user.balance = balance

        # etc
        self.post = 
        self.created_at = 
        self.giver = 
        self.taker = 
        self.save()
    '''
        
    




'''
# 계좌정보
class Account(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='등록시간')
    post = models.ForeignKey(Post, related_name='Transfer', null=True, on_delete=models.CASCADE)
    giver = models.ForeignKey(User, related_name="giver", on_delete=models.CASCADE, verbose_name="주는사람")
    taker = models.ForeignKey(User, related_name="taker", on_delete=models.CASCADE, verbose_name="받는사람")
    giver_balance = models.IntegerField(default=0, verbose_name='주는사람 계좌')
    taker_balance = models.IntegerField(default=0, verbose_name='받는사람 계좌')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # PositiveIntegerField : 0 또는 양수의 값
    balance = models.PositiveIntegerField(default=0, verbose_name='시간계좌')
    account_type_list = (
        ('주고싶어요','주고싶어요'),
        ('받고싶어요','받고싶어요')
        )
    account_type = models.CharField(max_length=10, choices=account_type_list)

    class Meta:
        ordering = ['-created_at']
'''