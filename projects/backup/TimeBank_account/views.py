from decimal import Context
from django.db.models.aggregates import Avg
from django.shortcuts import render, redirect,get_object_or_404, resolve_url
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
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from TimeBank_app.models import Post, Apply, Review, MainCategory
from .models import User, Account
import json
from datetime import datetime
from django.db.models import F, Sum, Count, Case, When, Q
from PIL import Image
import decimal
from django.template import loader


# test
def contact(request):
    return render(request, 'contact.html')




# img resizing
def rescale(image, width):
    img = Image.open(image)

    src_width, src_height = img.size
    src_ratio = float(src_height) / float(src_width)
    dst_height = round(src_ratio * width)

    img = img.resize((width, dst_height), Image.LANCZOS)
    img.save(image.name, 'PNG')
    image.file = img
    
    # 이게 없으면 attribute error 발생
    image.file.name = image.name

    return image




# 회원가입
def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        name = request.POST["name"]
        password = request.POST["password"]
        password_check = request.POST["password_check"]

        if request.FILES.get("image") is not None:
            image = request.FILES.get('image')

        # 비밀번호 재확인 불일치
        if password != password_check:
            return render(request, "register.html")

        # 새로운 유저 생성
        if request.FILES.get("image") is not None:
            user = User.object.create_user(username=username, email=email, password=password, name=name, image=image)
        else:
            user = User.object.create_user(username=username, email=email, password=password, name=name)
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        context = {'username':request.user}
    # return redirect('index')
    return render(request, 'register_profile.html', context)




# 회원가입 2단계 페이지- 프로필 설정
@login_required
def register_profile_page(request, username):
    user = request.user
    context = {
        "user": user,
        }
    return render(request, 'register_profile.html', context)




# 회원가입 2단계 - 프로필 설정
@login_required
def register_profile(request,username):
    user = get_object_or_404(User,username=username)

    user.contact = request.POST["contact"]
    user.birth = request.POST["birth"]
    # 나이 계산하기
    birth = user.birth
    birth = datetime.strptime(birth, '%Y-%m-%d')    # 문자열을 시간 객체로 바꾸기
    today = datetime.now()      # 현재시간 얻기
    user.user_age = today.year - birth.year

    user.gender = request.POST["gender"]
    user.give = request.POST.getlist('answersG[]')
    user.take = request.POST.getlist('answersT[]')
    user.about = request.POST["about"]
    user.save()
    return redirect('index')




# ID 중복 조회
def id_overlap_check(request):
    username = request.GET.get('username')
    try:
        # 중복 검사 실패
        user = User.objects.get(username=username)
    except:
        # 중복 검사 성공
        user = None
    if user is None:
        overlap = "pass"
    else:
        overlap = "fail"
    context = {'overlap': overlap}
    return JsonResponse(context)   





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
def profile(requset,username):
    user_profile = get_object_or_404(User,username=username)
    give = user_profile.give
    take = user_profile.take
    reviews = Review.objects.filter(author=user_profile)
    # 받은 거래
    recieved_reviews = Review.objects.filter(partner=user_profile)
    recieved_review_num = len(recieved_reviews)

    # 평균평점
    if recieved_review_num == 0:
        avg_star = 0
    else:
        avg_star = user_profile.star/recieved_review_num

    if 0<=avg_star<1:
        avg_star_view = 0
    elif 1<=avg_star<2:
        avg_star_view = 1
    elif 2<=avg_star<3:
        avg_star_view = 2
    elif 3<=avg_star<4:
        avg_star_view = 3
    elif 4<=avg_star<5:
        avg_star_view = 4
    elif avg_star==5:
        avg_star_view = 5

    plus_list = Account.objects.filter(giver= user_profile).aggregate(Sum('tok'))
    if plus_list.get('tok__sum') is None:
        plus_tok = 0
    else:
        plus_tok = round(plus_list.get('tok__sum'),2)
    
    minus_list = Account.objects.filter(taker= user_profile).aggregate(Sum('tok'))
    if plus_list.get('tok__sum') is None:
        minus_tok = 0
    else:
        minus_tok = round(minus_list.get('tok__sum'),2)


    context = {"user_profile":user_profile, 
                'username': username, 
                'plus_tok': plus_tok, 
                'minus_tok': minus_tok, 
                "avg_star": avg_star, 
                "avg_star_view": avg_star_view,
                "gives":give,
                "takes": take
                }
    return render(requset, "profile.html", context)




# 프로필 수정페이지 보기
@login_required
def profile_update_page(request,username):
    user = get_object_or_404(User,username=username)

    plus_list = Account.objects.filter(giver= user).aggregate(Sum('tok'))
    if plus_list.get('tok__sum') is None:
        plus_tok = 0
    else:
        plus_tok = round(plus_list.get('tok__sum'),2)
    
    minus_list = Account.objects.filter(taker= user).aggregate(Sum('tok'))
    if plus_list.get('tok__sum') is None:
        minus_tok = 0
    else:
        minus_tok = round(minus_list.get('tok__sum'),2)

    context = {"user_profile":user, 'username': username, 'plus_tok':plus_tok, 'minus_tok':minus_tok}
    return render(request, "profile_update.html", context)



# 프로필 수정
@login_required
def profile_update(request,username):
    user = get_object_or_404(User,username=username)

    user.name = request.POST["name"]
    user.contact = request.POST["contact"]
    
    if 'contactCk' in request.POST:
        user.contactCk = request.POST['contactCk']
    else:
        user.contactCk = False

    user.birth = request.POST["birth"]
    # user.user_age = request.POST["user_age"]
    # 나이 계산하기
    birth = user.birth
    birth = datetime.strptime(birth, '%Y-%m-%d')    # 문자열을 시간 객체로 바꾸기
    today = datetime.now()      # 현재시간 얻기
    user.user_age = today.year - birth.year
    user.gender = request.POST["gender"]
    user.about = request.POST["about"]
    user.give = request.POST.getlist('answersG[]')
    user.take = request.POST.getlist('answersT[]')
    user.save()
    return redirect('profile', user.username)



# 계좌번호 생성하기
def create_account_no(request):
    account = Account.create(request.user)
    account.save()
    account_no = account.account_no
    
    return render(request, "balance.html", {"account_no":account_no})



# 계좌 내역 보여주기
def account_history(request, username):
    user_profile = get_object_or_404(User,username=username)
    posts = Post.objects.all()
    # 내가 등록한 거래
    my_posts = posts.filter(author = user_profile)
    # 내가 신청한 거래
    regsiter_posts = Apply.objects.filter(to_user = user_profile)
    plus_list = Account.objects.filter(giver= user_profile).aggregate(Sum('tok'))
    if plus_list.get('tok__sum') is None:
        plus_tok = 0
    else:
        plus_tok = round(plus_list.get('tok__sum'),2)
    
    minus_list = Account.objects.filter(taker= user_profile).aggregate(Sum('tok'))
    if plus_list.get('tok__sum') is None:
        minus_tok = 0
    else:
        minus_tok = round(minus_list.get('tok__sum'),2)

 # 받은 거래
    recieved_reviews = Review.objects.filter(partner=user_profile)
    recieved_review_num = len(recieved_reviews)

    # 평균평점
    if recieved_review_num == 0:
        avg_star = 0
    else:
        avg_star = user_profile.star/recieved_review_num

    if 0<=avg_star<1:
        avg_star_view = 0
    elif 1<=avg_star<2:
        avg_star_view = 1
    elif 2<=avg_star<3:
        avg_star_view = 2
    elif 3<=avg_star<4:
        avg_star_view = 3
    elif 4<=avg_star<5:
        avg_star_view = 4
    elif avg_star==5:
        avg_star_view = 5

    context = {'user_profile':user_profile, 'my_posts': my_posts, 'regsiter_posts': regsiter_posts,
         'plus_tok':plus_tok, 'minus_tok':minus_tok, 'avg_star':avg_star, "avg_star_view":avg_star_view}
    return render(request, "account.html",context)




# 계좌내역 Account 모델 사용
@login_required
def balance(request, username):
    user_profile = get_object_or_404(User,username=username)
    accounts = Account.objects.filter(giver= user_profile) | Account.objects.filter(taker= user_profile)
    accounts = accounts.order_by('-timestamp')
    giver_balances = Account.objects.filter(giver=user_profile)
    
     # 받은 거래
    recieved_reviews = Review.objects.filter(partner=user_profile)
    recieved_review_num = len(recieved_reviews)

    # 평균평점
    if recieved_review_num == 0:
        avg_star = 0
    else:
        avg_star = user_profile.star/recieved_review_num

    if 0<=avg_star<1:
        avg_star_view = 0
    elif 1<=avg_star<2:
        avg_star_view = 1
    elif 2<=avg_star<3:
        avg_star_view = 2
    elif 3<=avg_star<4:
        avg_star_view = 3
    elif 4<=avg_star<5:
        avg_star_view = 4
    elif avg_star==5:
        avg_star_view = 5

    plus_list = Account.objects.filter(giver= user_profile).aggregate(Sum('tok'))
    if plus_list.get('tok__sum') is None:
        plus_tok = 0
    else:
        plus_tok = round(plus_list.get('tok__sum'),2)
    
    minus_list = Account.objects.filter(taker= user_profile).aggregate(Sum('tok'))
    if plus_list.get('tok__sum') is None:
        minus_tok = 0
    else:
        minus_tok = round(minus_list.get('tok__sum'),2)
    context = {'user_profile':user_profile,'accounts':accounts, 'giver_balances':giver_balances, 
                'plus_tok':plus_tok, 'minus_tok':minus_tok,'avg_star':avg_star, "avg_star_view":avg_star_view}
    return render(request, 'balance.html', context)





# 선물하기 유저 검색
@login_required
def balance_search(request, username):
    user_profile = get_object_or_404(User,username=username)
    accounts = Account.objects.filter(giver= user_profile) | Account.objects.filter(taker= user_profile)
    accounts = accounts.order_by('-timestamp')
    giver_balances = Account.objects.filter(giver=user_profile)
    
    # 받은 거래
    recieved_reviews = Review.objects.filter(partner=user_profile)
    recieved_review_num = len(recieved_reviews)

    # 평균평점
    if recieved_review_num == 0:
        avg_star = 0
    else:
        avg_star = user_profile.star/recieved_review_num

    if 0<=avg_star<1:
        avg_star_view = 0
    elif 1<=avg_star<2:
        avg_star_view = 1
    elif 2<=avg_star<3:
        avg_star_view = 2
    elif 3<=avg_star<4:
        avg_star_view = 3
    elif 4<=avg_star<5:
        avg_star_view = 4
    elif avg_star==5:
        avg_star_view = 5

    plus_list = Account.objects.filter(giver= user_profile).aggregate(Sum('tok'))
    if plus_list.get('tok__sum') is None:
        plus_tok = 0
    else:
        plus_tok = round(plus_list.get('tok__sum'),2)
    
    minus_list = Account.objects.filter(taker= user_profile).aggregate(Sum('tok'))
    if plus_list.get('tok__sum') is None:
        minus_tok = 0
    else:
        minus_tok = round(minus_list.get('tok__sum'),2)
    
    # 유저검색
    users = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        users = User.objects.all().filter(Q(username__contains=query))

    context = {
        'user_profile':user_profile,'accounts':accounts, 
        'giver_balances':giver_balances, 'plus_tok':plus_tok,
        'minus_tok':minus_tok,'avg_star':avg_star, "avg_star_view":avg_star_view,
        'users':users, 'query':query
        }
    return render(request, 'balance_search.html', context)




# 선물하기 
def gift(request, username):
    giver_name = request.POST['giver']
    giver = User.objects.get(username=giver_name)
    tok = decimal.Decimal(request.POST['tok'])

    if tok <= request.user.balance:
        account = Account()
        account.giver = giver
        account.taker = request.user
        account.giver.balance += decimal.Decimal(tok)
        account.taker.balance -= decimal.Decimal(tok)
        account.giver_balance = account.giver.balance
        account.taker_balance = account.taker.balance
        account.tok = tok
        account.mainwork = "선물하기"
        account.subwork = "선물하기"
        account.giver.save()
        account.taker.save()
        account.save()
        return redirect('balance', username)

    else:
        context = {
            'username': request.user.username,
            'error_msg': '계좌에 잔액이 부족합니다.',
            'user_profile': get_object_or_404(User,username=username)
        }
        return redirect('balance_search', username)







# 거래 후기 페이지 보기
def my_review(request, username):
    user_profile = get_object_or_404(User,username=username)
    
    post = Post.objects.filter(giver= user_profile) | Post.objects.filter(taker= user_profile) # 거래한 글
    
    reviews = Review.objects.filter(author=user_profile)    # 내가 작성한 거래
    recieved_reviews = Review.objects.filter(partner=user_profile)  # 받은 리뷰


    # 미작성 거래후기
    my_review = post & Post.objects.filter(status="완료확정")   #작성가능 리뷰
    ck_review = Review.objects.filter(post__in=my_review) # 리뷰작성여부 판단


    # 후기요약
    post_num = len(post)    #총 거래 횟수
    my_review_num = len(my_review)  # 완료한 거래확정수
    not_success_cks = Post.objects.filter(taker= user_profile) & Post.objects.filter(status="완료") #미완료 거래확정
    not_success_ck_num = len(not_success_cks)      # 미완료 거래확정 수
    review_num = len(reviews)       # 작성한 거래후기
    not_created_review_num = len(my_review)-len(reviews)  # 미작성 거래후기수
    recieved_review_num = len(recieved_reviews)    # 받은 거래후기



    if reviews:
        reviews = reviews
    else:
        reviews = None

    # 평균평점
    if recieved_review_num == 0:
        avg_star = 0
    else:
        avg_star = user_profile.star/recieved_review_num

    if 0<=avg_star<1:
        avg_star_view = 0
    elif 1<=avg_star<2:
        avg_star_view = 1
    elif 2<=avg_star<3:
        avg_star_view = 2
    elif 3<=avg_star<4:
        avg_star_view = 3
    elif 4<=avg_star<5:
        avg_star_view = 4
    elif avg_star==5:
        avg_star_view = 5
 
    plus_list = Account.objects.filter(giver= user_profile).aggregate(Sum('tok'))
    if plus_list.get('tok__sum') is None:
        plus_tok = 0
    else:
        plus_tok = round(plus_list.get('tok__sum'),2)
    
    minus_list = Account.objects.filter(taker= user_profile).aggregate(Sum('tok'))
    if plus_list.get('tok__sum') is None:
        minus_tok = 0
    else:
        minus_tok = round(minus_list.get('tok__sum'),2)

    context = {"user_profile":user_profile, "post_num":post_num, "review_num":review_num, "reviews":reviews, 'post':post, 'not_created_review_num':not_created_review_num,
                'plus_tok':plus_tok, "minus_tok":minus_tok, "recieved_reviews":recieved_reviews,"not_success_ck_num":not_success_ck_num
                ,"avg_star":avg_star,"avg_star_view":avg_star_view,"recieved_review_num":recieved_review_num
                ,"not_success_cks": not_success_cks,'reviews':reviews,'my_review_num':my_review_num, 'review_num':review_num
                ,"ck_review":ck_review}
    return render(request, 'my_review.html', context)



# 내가 쓴 거래후기 자세히보기
def my_review_detail(request, review_id):
    reviews = Review.objects.filter(pk=review_id)
    context = {"reviews":reviews}
    return render(request, "my_review_detail.html", context)








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




# 내가 신청한 글 완료하기
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



# 내가 쓴 글 중단하기
def stop(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.status = "중단"
    post.save()
    return redirect('/account/account')
