from django import forms

class PostForm(forms.Form):
    content = forms.CharField(
        error_messages={
            'required': '내용을 입력해주세요'
        },
        widget=forms.Textarea, label="내용")