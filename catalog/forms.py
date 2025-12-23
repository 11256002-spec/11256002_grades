from django import forms
from django.contrib.auth.models import User

class StudentRegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    full_name = forms.CharField(max_length=100)
    student_id = forms.CharField(max_length=20)
