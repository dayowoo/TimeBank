from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import auth
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import HttpResponse
from django.contrib import messages


# 홈화면
def index(request):
    return render(request, 'index.html')



# 회원가입
def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        userid = request.POST["userid"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        password_check = request.POST["pw_check"]
        image = request.FILES["image"]
        # 비밀번호 재확인 불일치
        if password != password_check:
            return render(request, "register.html")
        # 새로운 유저 생성
        user = User.objects.create_user(username=username, password=password, name=name, email=email, image=image)
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
            return render(request, "login.html")
        # 로그인 처리
        auth.login(request, user)
    return redirect("index")


# 로그아웃
def sign_out(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            auth.logout(request)
    return redirect('index')



# 프로필
@login_required
def profile(requset,username):
    user = get_object_or_404(User,username=username)

    return render(requset, "profile.html",{ "user_profile":user, 'username': username})


# 거래 내역
def account_history(request):
    return render(request, "account.html")
