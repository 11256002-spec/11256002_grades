from django import forms
from django.contrib.auth.models import User
from .models import Profile   # 匯入 Profile 模型

class StudentRegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label='帳號')
    password1 = forms.CharField(widget=forms.PasswordInput, label='密碼')
    password2 = forms.CharField(widget=forms.PasswordInput, label='確認密碼')
    full_name = forms.CharField(max_length=100, label='姓名')
    student_id = forms.CharField(max_length=20, label='學號')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('兩次輸入的密碼不一致')
        return cleaned_data

# ======================
# 個人資訊編輯表單
# ======================
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'avatar']   # 只允許修改姓名和頭像
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
