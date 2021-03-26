from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.utils import timezone
from TimeBank_app.models import Post, MainCategory, SubCategory
from TimeBank_account.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import re
from django.contrib import messages
from django.utils import timezone
from .forms import PostForm

# home
def index(request):
    return render(request, 'index.html')


def post_list(request):
    # order_by : 순서정렬 / 최신순
    posts = Post.objects.all().order_by('-id')
    return render(request, 'post_list.html', {'posts': posts})

def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            author = User.object.get(id=user_id)
            post = Post()
            post.content = form.cleaned_data['content']
            post.author = request.user
            post.save()

            return redirect('/post/post_list/')
    else:
        form = PostForm()
    return render(request, 'new_post.html', {'form':form})  




'''
# 신규 거래 등록 - 템플릿 보여주기
@login_required
def new(request):
    posts = Post.objects.all
    return render(request, 'new_post.html', {"posts":posts})

# 거래등록 - 데이터 저장
def create(request):
    
    start_time = request.GET["start_time"]
    end_time = request.GET["end_time"]
    service = request.GET["service"]
    location = request.GET["location"]
    main_work = request.GET["main_work"]
    sub_work = request.GET["sub_work"]
    content = request.GET["content"]
    
    post.start_time = start_time
    post.end_time = end_time
    post.start_time = start_time
    post.service = service
    post.location = location
    post.main_work = main_work
    post.sub_work = sub_work
    
    post.content = content
    post.time = timezone.now()
    post.save()
    return redirect('post_list')
    '''