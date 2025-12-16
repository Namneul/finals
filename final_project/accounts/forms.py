from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'real_name', 'location', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '아이디'}),
            'real_name': forms.TextInput(attrs={'placeholder': '이름 (예: 홍길동)'}),
            'location': forms.TextInput(attrs={'placeholder': '사는 지역 (예: 전주)'}),
            'email': forms.EmailInput(attrs={'placeholder': '이메일 (선택)'}),
        }