from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.contrib import auth


# 회원가입
@csrf_exempt
def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password1"]
        password_check = request.POST["password2"]
        
        # 비밀번호 재확인 불일치
        if password != password_check:
            return render(request, "register.html")
        # 새로운 유저 생성
        user = User.objects.create_user(username=username, password=password)
        auth.login(request, user)
    return redirect("http://127.0.0.1:8000")


# 로그인
@csrf_exempt
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
        #  로그인 처리
        auth.login(request, user)
    return redirect("http://127.0.0.1:8000")


# 로그아웃
def logout(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            auth.logout(request)
    return redirect("http://127.0.0.1:8000")


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
