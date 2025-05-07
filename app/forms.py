from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserSignupForm(UserCreationForm):
    father_name = forms.CharField(max_length=150, required=True, label="Father's Name")
    class Meta:
        model = User
        fields = ['username', 'father_name', 'password1', 'password2']
