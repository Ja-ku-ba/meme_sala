from django.forms import ModelForm
from .models import Account, Post
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['email', 'username', 'password1', 'password2']

class LoginForm(ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'password']

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']

