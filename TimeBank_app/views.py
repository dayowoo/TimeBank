from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.utils import timezone
from TimeBank_app.models import Post, MainCategory, SubCategory, MessageItem
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
from .forms import PostForm, MsgForm

# home
def index(request):
    return render(request, 'index.html')


# 거래글 목록
def post_list(request):
    # order_by : 순서정렬 / 최신순
    posts = Post.objects.all().order_by('-id')
    return render(request, 'post_list.html', {'posts': posts})


# 신규 거래 등록
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            author = User.object.get(id=username)
            post = Post()
            post.content = form.cleaned_data['content']
            post.author = request.user
            post.service = request.service
            post.save()

            return redirect('/post/post_list/')
    else:
        form = PostForm()
    return render(request, 'new_post.html', {'form':form})  










def test_btn(request):
    status = get_object_or_404(MessageItem, status="wait")
    is_cliked = status.filter()
    pass

# 신청하기
def send_message(request):
    form = MsgForm()
    return render(request, 'testmsg_form.html', {'form': form})





#########
'''
class ButtonView:
    def __init__(self, show_btn):
        self.show_btn = show_btn

    def applicant_mode()
    pass
'''













# 신청 내용 저장
def create_message(request):  

        posts = Post.objects.all().order_by('-id')
        return render(request, 'post_list.html', {'posts': posts})

'''

def create_message(request):
    show_btn = True
    btn_msg = "신청하기"

    context = {
                'show_btn': show_btn,
                'btn_msg': btn_msg,
            }
    
    post = Post()
    post.author = request.user
    post.service = request.service
    post.save()

    return render(request, "post_list_tmp2.html", context)
'''




'''
# 신청하기
#@login_required(login_url='login')
def send_message(request, post_id):
    post = Post.objects.get(pk=post_id)
    if post.author != request.user:
        try:
            # 장바구니는 user 를 FK 로 참조하기 때문에 save() 를 하기 위해 user 가 누구인지도 알아야 함
            message = MessageItem.objects.get(post_id=post.pk, user__id=request.user.pk)
            if message:
                if message.post.content == post.content:
                    message.quantity += 1
                    message.save()
        except MessageItem.DoesNotExist:
            user = User.objects.get(pk=request.user.pk)
            message = MessageItem(
                user=user,
                post=post,
                message_list=1,
            )
            message.save()
        return redirect('profile')
    else:
        messages.error(request, '자신의 글은 신청할 수 없습니다.')
 '''       


# 대기중



# 거래 진행중



# 거래 완료


# 거래 중단
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