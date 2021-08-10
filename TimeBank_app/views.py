from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from TimeBank_app.models import Comment, Post, Apply, ReComment, Review
from TimeBank_account.models import Account
from TimeBank_account.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.paginator import Paginator
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import re
from django.contrib import messages
from django.utils import timezone
# from .forms import PostForm, MsgForm
import json
import decimal
from datetime import datetime
import time





# home
def index(request):
    time_1 = datetime.strptime('05:00 AM', "%H:%M %p")
    time_2 = datetime.strptime('10:45 AM', "%H:%M %p")

    time_difference = time_2 - time_1
    second = str(time_difference)[:4]
    print(second)
    hour = int(second[:1])*60
    minute = int(second[2:4])
    sum_tok = hour + minute
    tok = sum_tok / 60
    print(round(tok,2))
    
    print(type(time_difference))    # 'datetime.timedelta'
    print(type(str(time_difference)))     # 5:00:00 ->str
    return render(request, 'index.html')


# 새 글 작성 페이지
def new_post(request):
    return render(request, 'new_post.html')



# 새 글 작성 POST
def create(request):
    if(request.method == 'POST'):
        post = Post()
        post.date = request.POST.get('date')
        post.start_time = request.POST.get('start_time')
        post.end_time = request.POST.get('end_time')
        post.service = request.POST['service']
        post.location = request.POST['location']
        post.mainwork = request.POST['mainwork']
        post.subwork = request.POST['subwork']
        post.content = request.POST['content']
        post.author = request.user
        post.tok = request.POST['tok']
        
        if request.FILES.get("image") is not None:
            post.image = request.FILES.get('image')

        post.status = '대기'
        post.save()
    if post.service == "주고싶어요":
        post.giver = request.user
    else :
        post.taker = request.user
    post.save()
    return redirect('post_list')




# 글 수정페이지 보여주기
def update_page(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {'post':post}
    return render(request, 'post_update.html', context)



# 글 수정
def update(request, post_id):
    post = Post.objects.get(pk=post_id)

    if(request.method == 'POST'):
        post.date = request.POST['date']
        post.start_time = request.POST['start_time']
        post.end_time = request.POST['end_time']
        post.service = request.POST['service']
        post.location = request.POST['location']
        post.mainwork = request.POST['mainwork']
        post.subwork = request.POST['subwork']
        post.content = request.POST['content']
        post.author = request.user
        post.tok = request.POST['tok']
        post.status = '대기'
        post.save()
    if post.service == "주고싶어요":
        post.giver = post.author
    else :
        post.taker = post.author
    post.save()
    return redirect('post_detail', post_id)




# 글 삭제
def delete(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    return redirect('post_list')





# 거래글 목록
def post_list(request):
    # order_by : 순서정렬 / 최신순
    posts = Post.objects.all().order_by('-id')
    return render(request, 'post_list.html', {'posts':posts})




#### AJAX ####
def post_ajax(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)
    user = request.user.username
    content = {'content':post.content, 'author':post.author.username, 'id':post.id, 'user': user}
    return HttpResponse(json.dumps(content), content_type="application/json")




# 자세히 보기
def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post.id)
    account = Account.objects.filter(post=post.id)
    reviews = Review.objects.filter(post=post.id)
    applies = Apply.objects.filter(from_post=post)
    
    # 신청한 유저 확인
    apply_list = Apply.objects.filter(from_post=post).values('to_user')
    apply_name = []
    for i in range(0,len(apply_list)):
        apply_name.append(apply_list[i]['to_user'])

    
    btn_msg = post.status
    success_btn = "완료확정"
    
    if post.service == "받고싶어요":
        post.taker = post.author
        
    if post.status == "진행":
        if post.taker == request.user:
            btn_msg = "완료하기"
        else:               
            btn_msg = "승인대기"

    partner = [str(post.taker), str(post.giver)]
    context = {'post':post, 'btn_msg':btn_msg, 'comments':comments, 'applies':applies, 'partner':partner,
                 'reviews':reviews, 'success_btn':success_btn, 'account':account, 'apply_list':apply_list,
                 'apply_name':apply_name}
    return render(request, "post_detail.html", context)




# 신청하기
def apply(request, post_id):
    from_post = Post.objects.get(pk = post_id)
    to_user = request.user
    apply, created = Apply.objects.get_or_create(from_post=from_post, to_user=to_user)

    if created:
        message = '신청 완료'
        status = 1
    else:
        apply.delete()
        message = '신청 취소'
        status = 0

    context = {
        'message': message,
        'status': status,
    }
    return redirect('post_detail', post_id)




# 지원자 선택하기 (대기->진행)
def choice(request, post_id, user_id):
    
    post = Post.objects.get(pk=post_id)
    selection = request.POST['choice']
    applicant = Apply.objects.get(from_post=post_id, to_user=selection)

    post.status = "진행"

    if post.service == "주고 싶어요":
        post.giver = post.author
        post.taker = applicant.to_user
    else:
        post.giver = applicant.to_user
        post.taker = post.author
        
    post.save()
    applicant.save()

    return redirect("post_detail", post_id)




# 진행 -> 완료하기
def success(request, post_id, user_id):
    post = Post.objects.get(pk=post_id)
    post.status = "완료"
    post.save()
    return redirect('post_detail', post_id)




# 완료 확정하기 
def success_ck(request, post_id, user_id):
    post = Post.objects.get(pk=post_id)
    
    account = Account()
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']
    
    time_start = datetime.strptime(start_time, "%H:%M %p")
    time_end = datetime.strptime(end_time, "%H:%M %p")
    time_difference = time_end - time_start
    sec_del = str(time_difference)[:4]
    hour = int(sec_del[:1])*60
    minute = int(sec_del[2:4])
    sum_time = hour + minute
    tok = round(sum_time/60, 2)

    post.status = "완료확정"
    post.giver.balance += decimal.Decimal(tok)
    post.taker.balance -= decimal.Decimal(tok)
    post.save()
    post.taker.save()
    post.giver.save()

    account.post = post
    account.giver_balance = post.giver.balance
    account.taker_balance = post.taker.balance
    account.giver = post.giver
    account.taker = post.taker
    account.tok = decimal.Decimal(tok)
    account.mainwork = post.mainwork
    account.subwork = post.subwork
    account.giver.save()
    account.taker.save()
    account.save()

    btn_success_ck = "완료확정"
    if request.user == post.taker:
        btn_success_ck = "완료확정"
    else:
        btn_success_ck = "완료"

    return redirect('post_detail', post_id)


'''
# 완료 확정하기 
def success_ck(request, post_id, user_id):
    post = Post.objects.get(pk=post_id)
    account = Account()
    tok = request.POST['tok']
    post.status = "완료확정"
    post.giver.balance += decimal.Decimal(tok)
    post.taker.balance -= decimal.Decimal(tok)
    post.save()
    post.taker.save()
    post.giver.save()

    account.post = post
    account.giver_balance = post.giver.balance
    account.taker_balance = post.taker.balance
    account.giver = post.giver
    account.taker = post.taker
    account.tok = decimal.Decimal(tok)
    account.mainwork = post.mainwork
    account.subwork = post.subwork
    account.giver.save()
    account.taker.save()
    account.save()


    btn_success_ck = "완료확정"
    if request.user == post.taker:
        btn_success_ck = "완료확정"
    else:
        btn_success_ck = "완료"

    return redirect('post_detail', post_id)
'''



# 진행 -> 중단하기
def stop(request, post_id, user_id):
    post = Post.objects.get(pk=post_id)
    post.status = "중단"
    post.save()
    return redirect('post_detail', post_id)






# 댓글 등록하기
@login_required
def create_comment(request, post_id):
    comment = Comment()
    comment.content = request.POST['content']
    comment.post = get_object_or_404(Post, pk=post_id)
    comment.author = request.user
    comment.save()
    return redirect('post_detail', post_id)




# 댓글 삭제하기
@login_required
def delete_comment(request, post_id, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    return redirect("post_detail", post_id)


# 답글 달기
@login_required
def create_recomment(request, post_id, comment_id):
    recomment = ReComment()
    recomment.content = request.POST['recontent']
    recomment.comment = get_object_or_404(Comment, pk=comment_id)
    recomment.author = request.user
    recomment.save()
    return redirect('post_detail', post_id)




# 답글 삭제
@login_required
def delete_recomment(request, post_id, recomment_id):
    recomment = ReComment.objects.get(pk=recomment_id)
    recomment.delete()
    return redirect('post_detail', post_id)





# 리뷰 작성 페이지
def new_review(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {'post':post}
    return render(request, "new_review.html", context)




# 리뷰 작성하기 (완료 확정하기)
def create_review(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        if request.user == post.giver:
            partner = post.taker
        else:
            partner = post.giver
        review = Review()
        review.post = get_object_or_404(Post, pk=post_id)
        review.author = request.user
        review.partner = partner
        review.content = request.POST['content']
        review.star = request.POST['star']
        review.image = request.FILES["image"]
        review.save()
        
        review.partner.star = review.star
        review.partner.save()
        return redirect('post_detail', post_id)



# 리뷰 자세히보기
def review_detail(request, post_id, review_id):
    post = Post.objects.get(pk=post_id)
    review = Review.objects.get(pk=review_id)
    context = {'post':post, 'review':review}
    return render(request, "review_detail.html", context)



# 리뷰 수정페이지 보기
@login_required
def review_update_page(request, post_id, review_id):
    post = Post.objects.get(pk=post_id)
    review = Review.objects.get(pk=review_id)
    context = {'post':post, 'review':review}
    return render(request, "review_update.html", context)



# 리뷰 수정하기
def review_update(request, post_id, review_id):
    post = Post.objects.get(pk=post_id)
    review = Review.objects.get(pk=review_id)
    
    review.content = request.GET["content"]
    review.star = request.GET["star"]
    # review.image = request.POST["image"]
    review.save()

    return redirect('review_detail', post_id, review_id)



# 리뷰 삭제하기
def review_delete(request, post_id, review_id):
    review = Review.objects.get(pk=review_id)
    review.delete()
    return redirect('post_detail', post_id)


# # 지원하기
# @require_POST
# def apply(request):
#     id = request.POST.get('pk', None) 
#     post = get_object_or_404(Post, pk=id)
#     post_apply, post_apply_created = post.apply_set.get_or_create(username=request.user)

#     if not post_apply_created:
#         post_apply.delete()
#         message = "신청 취소"
#     else:
#         message = "신청 완료"

#     context = {'apply_count': post.apply_count,
#                'message': message,
#                 }

#     return HttpResponse(json.dumps(context), content_type="application/json")










'''
# 진행
def progress_ajax(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)
    message = "신청완료"
    post.status = '진행'
    post.applicant = request.user.username
    post.save()
    content = {
        'post_status': post.status,
        'message': message,
        'applicant': request.user.username
    }
    return HttpResponse(json.dumps(content), content_type="application/json")
'''

'''
# 신규 거래 등록
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user')
            user = User.objects.get(pk)
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
'''

'''
# 신청하기
@login_required
@require_POST
def send_msg(request):
    from_post = post.id
    pk = request.POST.get('pk')
    to_user = get_object_or_404(User, pk=pk)
    relation_created = Relation.objects.get_or_create(from_user=from_user, to_user=to_user)

    if created:
        message = '팔로우 시작!'
        status = 1

    return render('post_list.html')
'''
    



'''
# 신청 내용 저장
def create_message(request):  
    posts = Post.objects.get(pk=post.id)
    try:
    # user 를 FK 로 참조하기 때문에 save() 를 하기 위해 user 가 누구인지도 알아야 함
        message = MessageItem.objects.get(post_id=post.id, user__id=request.user.pk)
        if message:
            if message.post.id == post.id:
                message.message_list += 1
                message.save()
    except MessageItem.DoesNotExist:
        user = User.objects.get(pk=request.user.pk)
        message = MessageItem(
            user=user,
            post=post,
            message_list=1,
        )
        message.save()
    return redirect('account')
#        return render(request, 'post_list.html', {'posts': posts})
'''









#########
'''
class ButtonView:
    def __init__(self, show_btn):
        self.show_btn = show_btn

    def applicant_mode()
    pass
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




        