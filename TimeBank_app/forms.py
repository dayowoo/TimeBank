from django import forms

class PostForm(forms.Form):
    date = forms.DateTimeField(widget=forms.DateTimeField, label="연-월-일")
    content = forms.CharField(
        error_messages={
            'required': '내용을 입력해주세요'
        },
        widget=forms.Textarea, label="내용")
