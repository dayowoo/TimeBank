from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Comment, ReComment
from django.db.models import Q
from django.contrib.auth.decorators import login_required



# 거래글 목록
def board_list(request):
    # order_by : 순서정렬 / 최신순
    boards = Board.objects.all().order_by('-id')
    return render(request, 'board_list.html', {'boards':boards})


# 검색
def board_search(request):
    boards = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        boards = Board.objects.all().filter(Q(title__contains=query))
    context = {
        'boards': boards,
        'query': query
    }
    return render(request, 'board_search.html', context)




# 새 글 작성 페이지
def board_new(request):
    return render(request, 'board_new.html')


# 새 글 작성
# 새 글 작성 POST
def board_create(request):
    if(request.method == 'POST'):
        board = Board()
        board.category = request.POST['category']
        board.title = request.POST['title']
        board.author = request.user
        board.content = request.POST['content']        
        if request.FILES.get("image") is not None:
            board.image = request.FILES.get('image')
        board.save()
    return redirect('board_list')




# 게시판 자세히보기
def board_detail(request, board_id):
    board = Board.objects.get(pk=board_id)    
    comments = Comment.objects.filter(post=board)
    recomments = ReComment.objects.filter(comment__in=comments)

    #recomments =comments.recomment.all()

    context = {
        'board': board,
        'comments': comments,
        'recomments': recomments
    }
    return render(request, "board_detail.html", context)





# 글 수정페이지 보여주기
def board_update_page(request, board_id):
    board = Board.objects.get(pk=board_id)
    context = {'board':board}
    return render(request, 'board_update_page.html', context)




    
# 글 수정하기
def board_update(request, board_id):
    board = Board.objects.get(pk=board_id)

    if(request.method == 'POST'):
        board.category = request.POST['category']
        board.title = request.POST['title']
        board.content = request.POST['content']
        board.save()
    return redirect('board_detail', board_id)




# 글 삭제
def board_delete(request, board_id):
    board = Board.objects.get(pk=board_id)
    board.delete()
    return redirect('board_list')



# 댓글 달기
def create_comment(request, board_id):
    comment = Comment()
    comment.post = get_object_or_404(Board, pk=board_id)
    comment.author = request.user
    comment.content = request.POST['content']

    comment.save()
    return redirect('board_detail', board_id)




# 댓글 수정
def update_comment(request, board_id):
    comment = Board.objects.get(pk=board_id)
    if(request.method == 'POST'):
        comment.content = request.POST['content']
        comment.save()
    return redirect('board_detail', board_id)
    


# 댓글 삭제하기
@login_required
def delete_comment(request, board_id, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    return redirect("board_detail", board_id)




# 답글 달기
def create_recomment(request, board_id, comment_id):
    recomment = ReComment()
    recomment.comment = get_object_or_404(Comment, pk=comment_id)
    recomment.author = request.user
    recomment.content = request.POST['recomment']
    
    re_comment = Comment.objects.get(pk=comment_id)
    author = re_comment.author
    recomment.mention = '@{0}'.format(author)

    recomment.save()
    return redirect('board_detail', board_id)



# 답글 삭제하기
@login_required
def delete_recomment(request, board_id, comment_id, recomment_id):
    recomment = ReComment.objects.get(pk=recomment_id)
    recomment.delete()
    return redirect("board_detail", board_id)



# 답답글 달기
def create_rerecomment(request, board_id, comment_id, recomment_id):
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
    return redirect('board_detail', board_id)