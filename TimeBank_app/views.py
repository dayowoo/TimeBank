from django.shortcuts import render
from TimeBank_account import views

# home
def index(request):
    return render(request, 'index.html')

# 신규 거래 등록
def create(request):
    return render(request, 'new_post.html')

