'''
from django import forms
from TimeBank_app.models import MessageItem

class PostForm(forms.Form):
    date = forms.DateTimeField(widget=forms.DateTimeField, label="연-월-일")
    start_time = forms.TimeField(widget=forms.TimeField, label="시작시간")
    end_time = forms.TimeField(widget=forms.TimeField, label="종료시간")
    location = forms.CharField(widget=forms.CharField, label="장소")
    created_at = forms.DateTimeField(widget=forms.DateTimeField, label="작성시간")
    tok = forms.IntegerField(widget=forms.IntegerField, label="거래톡")
    content = forms.CharField(
        error_messages={
            'required': '내용을 입력해주세요'
        },
        widget=forms.Textarea, label="내용")


class MsgForm(forms.Form):
    model = MessageItem
    fileds = ['author', 'post', 'status', 'applicant']
'''


