from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Comment, ReComment, Deal
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from TimeBank_account.models import Account
import decimal


# Create your views here.
def shop_list(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, "shop_list.html", context)

def product_new(request):
    return render(request, "product_new.html")


# 새 글 작성 POST
@login_required
def product_create(request):
    if(request.method == 'POST'):
        product = Product()
        product.location = request.POST['location']
        product.tok = request.POST['tok']
        product.category = request.POST['category']
        product.title = request.POST['title']
        product.author = request.user
        product.content = request.POST['content']        
        if request.FILES.get("image") is not None:
            product.image = request.FILES.get('image')
        product.save()
    return redirect('shop_list')





# 자세히보기
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    comments = Comment.objects.filter(product=product)
    recomments = ReComment.objects.filter(comment__in=comments)

    applies = Deal.objects.filter(from_post=product)
    
    # 신청한 유저 확인
    apply_list = Deal.objects.filter(from_post=product).values('to_user')
    apply_name = []
    for i in range(0,len(apply_list)):
        apply_name.append(apply_list[i]['to_user'])

    context = {
        'product': product,
        'comments': comments,
        'recomments': recomments,
        'applies': applies,
        'apply_name': apply_name
    }
    return render(request, 'product_detail.html', context)




# 댓글 달기
@login_required
def create_product_comment(request, product_id):
    comment = Comment()
    comment.product = get_object_or_404(Product, pk=product_id)
    comment.author = request.user
    comment.content = request.POST['content']
    comment.save()
    return redirect('product_detail', product_id)






# 댓글 삭제하기
@login_required
def delete_product_comment(request, product_id, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    return redirect('product_detail', product_id)





#답글 달기
@login_required
def create_product_recomment(request, product_id, comment_id):
    recomment = ReComment()
    recomment.comment = get_object_or_404(Comment, pk=comment_id)
    recomment.author = request.user
    recomment.content = request.POST['recomment']
    
    re_comment = Comment.objects.get(pk=comment_id)
    author = re_comment.author
    recomment.mention = '@{0}'.format(author)

    recomment.save()
    return redirect('product_detail', product_id)



# 답글 삭제하기
@login_required
def delete_product_recomment(request, product_id, comment_id, recomment_id):
    recomment = ReComment.objects.get(pk=recomment_id)
    recomment.delete()
    return redirect("product_detail", product_id)



# 답답글 달기
@login_required
def create_product_rerecomment(request, product_id, comment_id, recomment_id):
    recomment = ReComment()
    re_comment = ReComment.objects.get(pk=recomment_id)
    author = re_comment.author

    # if author is None:
    #     comment = Comment.objects.get(pk=comment_id)
    #     recomment.mention = '@{0}'.format(comment.author)
    # else:
    #     recomment.mention = '@{0}'.format(author)

    recomment.comment = Comment.objects.get(pk=comment_id)
    recomment.reply = get_object_or_404(ReComment, pk=recomment_id)
    recomment.author = request.user
    recomment.content = request.POST['recomment']
    recomment.mention = '@{0}'.format(author)
 
    recomment.save()
    return redirect('product_detail', product_id)




# 신청하기
@login_required
def product_apply(request, product_id):
    from_post = Product.objects.get(pk = product_id)
    to_user = request.user
    apply, created = Deal.objects.get_or_create(from_post=from_post, to_user=to_user)

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
    return redirect('product_detail', product_id)



# 지원자 선택하기 (대기->진행)
@login_required
def product_choice(request, product_id, user_id):
    
    product = Product.objects.get(pk=product_id)
    selection = request.POST['choice']
    applicant = Deal.objects.get(from_post=product_id, to_user=selection)

    product.status = "진행"
    product.seller = product.author
    product.buyer = applicant.to_user
    product.save()
    applicant.save()

    return redirect("product_detail", product_id)


# 거래 완료하기
@login_required
def proudct_success(request, product_id, user_id):
    product = Product.objects.get(pk=product_id)
    product.status = "완료"
    product.save()
    return redirect('product_detail', product_id)



# 거래 중단하기
@login_required
def product_stop(request, product_id, user_id):
    product = Product.objects.get(pk=product_id)
    product.status = "중단"
    product.save()
    return redirect('product_detail', product_id)



# 거래 확정하기
@login_required
def product_success_ck(request, product_id, user_id):
    product = Product.objects.get(pk=product_id)
    tok = request.POST['tok']
    account = Account()

    # 계좌저축
    product.status = "완료확정"
    product.seller.balance += decimal.Decimal(tok)
    product.buyer.balance -= decimal.Decimal(tok)
    product.save()
    product.seller.save()
    product.buyer.save()
    
    account.product = product
    account.giver_balance = product.seller.balance
    account.taker_balance = product.buyer.balance
    account.giver = product.seller
    account.taker = product.buyer
    account.tok = decimal.Decimal(tok)
    account.mainwork = "중고거래"
    account.subwork = product.category
    account.giver.save()
    account.taker.save()
    account.save()

    return redirect('product_detail', product_id)