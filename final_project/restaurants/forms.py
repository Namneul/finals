from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'res_name', 'res_address', 'res_category', 'res_link', 'image', 'content']
        widgets = {
            'res_name': forms.TextInput(attrs={'readonly': 'readonly', 'placeholder': '식당 검색 버튼을 이용해주세요'}),
            'res_address': forms.HiddenInput(),
            'res_category': forms.HiddenInput(),
            'res_link': forms.HiddenInput(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']