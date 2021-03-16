from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.utils import timezone
from .models import *
from TimeBank_account.models import *
#from .forms import *
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

# home
def index(request):
    return render(request, 'index.html')


# 신규 거래 등록
@login_required
def create(request):
    if request.method=="POST":
        form = NewPost(request.POST, request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.created_at = timezone.now()
            post.updated_at = timezone.now()
            post.author=request.user
            post.save()
            content = form.cleaned_data.get('content')

    return render(request, 'new_post.html', {"form":form})

