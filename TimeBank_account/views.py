from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import get_user_model
from TimeBank_app.views import *
from django.contrib.auth.hashers import make_password, check_password


def home(request):
    user_id = request.session.get('user')

    if user_id:
        user = User.objects.get(pk=user_id)
        return HttpResponse(user.username)
        
    return render(request, 'index.html')




# 회원가입
@csrf_exempt
def register(request):
    # 단순히 페이지에 들어오는 경우
    if request.method == "GET":
        return render(request, 'register.html')
    # 등록버튼 클릭
    elif request.method == "POST":
        user_id = request.POST["user_id"] #id
        email = request.POST["email"]
        username = request.POST["username"] #이름
        password = request.POST["password"]
        password_check = request.POST["pw_check"]
        image = request.FILES["image"]

        res_data = {}
        # 비밀번호 재확인 불일치
        if password != password_check:
            res_data ['error'] = '비밀번호가 다릅니다.'

        # 새로운 유저 생성
        user = User(
            user_id=user_id, password=password,
            username=username, email=email, image=image
            )
        user.save()

    return render(request, 'login.html', res_data)


# 로그인
@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        res_data = {}
        if not (user_id and password):
            res_data['error'] = '모든 값을 입력하세요'
        else:
            user = get_object_or_404(User, pk=user_id)
            if check_password(password, User.password):
                #비밀번호 일치, 로그인 처리
                request.session['user'] = User.id 
                return redirect('/')
            #비밀번호 불일치, 로그인 실패
            else:
                res_data['error'] = '비밀번호가 틀렸습니다'
        return render(request, 'login.html', res_data)

    #     # 존재하지 않는 user
    #     if user is None:
    #         return render(request, "login.html")
    #     #  로그인 처리
    #     auth.login(request, user)
    # return render(request,'index.html')

# 로그아웃
def logout(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            auth.logout(request)
    return redirect("index")

# 프로필
@login_required
def profile(requset,username):
    user = get_object_or_404(User,username=username)

    return render(requset, "profile.html",{ "user_profile":user, 'username': username})

# 거래 내역
def account_history(request):
    return render(request, "account.html")

# @csrf_exempt
# def register(request):
#     if request.method == 'POST':
#         if request.POST['password1'] == request.POST['password2']:
#             user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
#             auth.login(request, user)
#             return redirect('http://127.0.0.1:8000')
#     return render(request, 'register.html')


# # 로그인
# @csrf_exempt
# def login(request):
#     if request.method =='POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('http://127.0.0.1:8000')    
#         else:
#             return render(request, 'login.html', {'error':'username or password is incorrect'})

#     else:
#         return render(request, 'login.html')
