from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import auth
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import HttpResponse
from django.contrib import messages
from TimeBank_app.models import Post
from .models import User, Account
import json


# 홈화면
def index(request):
    return render(request, 'index.html')



# 회원가입
def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        name = request.POST["name"]
        password = request.POST["password"]
        password_check = request.POST["pw_check"]
        image = request.FILES["image"]

        # 비밀번호 재확인 불일치
        if password != password_check:
            return render(request, "register.html")
        # 새로운 유저 생성
        user = User.object.create_user(username=username, email=email, password=password, name=name, image=image)
        auth.login(request, user)
    return redirect('index')


# 로그인
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        # 존재하지 않는 user
        if user is None:
            return render(request, "login.html", {"msg": "로그인 실패!"})
        # 로그인 처리
        auth.login(request, user)
    return redirect('index')


# 로그아웃
def logout(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            auth.logout(request)
    return redirect('index')



# 프로필
@login_required
def profile(requset,username):
    user = get_object_or_404(User,username=username)
    return render(requset, "profile.html", {"user_profile":user, 'username': username})


# 프로필 수정페이지 보기
@login_required
def profile_update_page(request,username):
    user = get_object_or_404(User,username=username)
    return render(request, "profile_update.html", {"user_profile":user, 'username': username})


# 프로필 수정
@login_required
def profile_update(request,username):
    user = get_object_or_404(User,username=username)
    #user.email = request.POST["email"]
    user.contact = request.POST["contact"]
    user.birth = request.POST["birth"]
    user.user_age = request.POST["user_age"]
    user.gender = request.POST["gender"]
    user.about = request.POST["about"]
    user.save()
    return render(request, "profile.html", {"user_profile":user, 'username': username})



# 계좌번호 생성하기
def create_account_no(request):
    account = Account.create(request.user)
    account.save()
    account_no = account.account_no
    return render(request, "balance.html", {"account_no":account_no})



# 계좌 내역 보여주기
def account_history(request):
    posts = Post.objects.all()
    # 내가 등록한 거래
    my_posts = posts.filter(author = request.user)
    # 내가 신청한 거래
    regsiter_posts = posts.filter(applicants = request.user)
    return render(request, "account.html", {'my_posts': my_posts, 'regsiter_posts': regsiter_posts})



'''
# 고치고 있는 코드
@login_required
def balance(request):
    user = request.user
    balance = int(user.balance)

    post = post.account.objects.all()
    success = post.filter(status = "완료")
    # 완료, giver or taker
    success_posts = success.filter(giver = str(request.user))

    plus_toks = 0
    minus_toks = 0
    
    post.giver.account.update()
    post.taker.account.update()



    # +인 경우
    if str(request.user) == str(success_posts.giver):
        plus_toks = int(success_posts.tok)
        balance = balance + plus_toks
    elif str(request.user) == str(success_posts.taker):
        minus_toks = int(success_posts.tok)
        balance = balance - minus_toks
    return render(request, "balance.html", {'success_posts': success_posts, 'balance':balance, 'plus_toks':plus_toks, 'minus_toks':minus_toks})



# 거래글 목록
def post_list(request):
    # order_by : 순서정렬 / 최신순
    posts = Post.objects.all().order_by('-id')
    return render(request, 'post_list.html', {'posts': posts})
'''

# 계좌내역 Account 모델 사용
@login_required
def balance(request):
    accounts = Account.objects.filter(giver=request.user) | Account.objects.filter(taker=request.user)
    return render(request, 'balance.html', {'accounts':accounts})





'''
# 잔액 조회
@login_required
def balance(request):
    post = Post.objects.all()
    user = request.user
    username = str(request.user)
    balance = int(user.balance)
    success = post.filter(status = "완료") 
    success_posts = success.filter(giver = request.user) or success.filter(taker = request.user)
    if success_posts.filter(service = "주고싶어요"):
        if request.user == success_posts.giver:
            balance = balance + success_posts.tok
    elif success_posts.filter(service="받고싶어요"):
        if request.user == success_posts.giver:
            balance = balance + success_posts.tok
    # -인 경우        
    if success_posts.filter(service = "주고싶어요"):
        if request.user == success_posts.taker:
            balance = balance - success_posts.tok
    elif success_posts.filter(service="받고싶어요"):
        if request.user == success_posts.taker:
            balance = balance - success_posts.tok
    return render(request, "balance.html", {'username':username, 'success_posts': success_posts, 'balance':balance})
'''







# 내가 신청한 거래 자세히보기
def my_register_detail(request, post_id):
    register_post = Post.objects.get(pk=post_id)
    btn_msg = register_post.status
    if register_post.status == "진행":
        if register_post.taker == request.user:
            btn_msg = "완료하기"
        else:
            btn_msg = "승인대기"
    return render(request, "my_register_detail.html", {"register_post":register_post, 'btn_msg':btn_msg})




'''
# 내가 신청한 글 완료하기
def reg_success(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.status = "완료"
    account = Account()
    user = request.user
    if post.giver == request.user:
        user.balance += post.tok
        account.balance = user.balance
        post.taker.balance -= post.tok
    elif post.taker == request.user:
        user.balance -= post.tok
        account.balance = user.balance
        post.giver.balance += post.tok
    account.giver = post.giver
    account.taker = post.taker
    account.tok = post.tok
    account.mainwork = post.mainwork
    account.subwork = post.subwork
    post.save()
    post.taker.save()
    post.giver.save()
    user.save()
    account.save()
    return redirect('/account/account')
'''




def reg_success(request, post_id):
    post = Post.objects.get(pk=post_id)
    account = Account()
    user = request.user
    post.status = "완료"
    post.giver.balance += post.tok
    post.taker.balance -= post.tok
    post.save()
    post.taker.save()
    post.giver.save()

    account.giver_balance = post.giver.balance
    account.taker_balance = post.taker.balance
    account.giver = post.giver
    account.taker = post.taker
    account.tok = post.tok
    account.mainwork = post.mainwork
    account.subwork = post.subwork
    user.save()
    account.save()
    return redirect('/account/account')

# 내가 신청한 글 중단하기
def reg_stop(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.status = "중단"
    post.save()
    return redirect('/account/account')



# 내가 쓴글 자세히보기
def my_post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    btn_msg = post.status
    if post.status == "진행":
        if post.taker == request.user:
            btn_msg = "완료하기"
        else:
            btn_msg = "승인대기"
    return render(request, "my_post_detail.html", {'post':post, 'btn_msg':btn_msg})



# 내가 쓴 글 완료하기
def success(request, post_id):
    post = Post.objects.get(pk=post_id)
    # account 계좌 생성
    account = Account()
    user = request.user
    post.status = "완료"
    post.giver.balance += post.tok
    post.taker.balance -= post.tok
    post.save()
    post.taker.save()
    post.giver.save()

    account.giver_balance = post.giver.balance
    account.taker_balance = post.taker.balance
    account.giver = post.giver
    account.taker = post.taker
    account.tok = post.tok
    account.mainwork = post.mainwork
    account.subwork = post.subwork
    user.save()
    account.save()
    return redirect('/account/account')




'''
# 내가 쓴 글 완료하기
def success(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user
    post.status = "완료"
    if post.giver == request.user:
        user.balance += post.tok
        post.taker.balance -= post.tok
    elif post.taker == request.user:
        user.balance -= post.tok
        post.giver.balance += post.tok
    post.save()
    post.taker.save()
    post.giver.save()
    user.save()
    return redirect('/account/account')
'''


# 내가 쓴 글 중단하기
def stop(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.status = "중단"
    post.save()
    return redirect('/account/account')





