from django.forms import ModelForm
from .models import Account, Post
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Wymagane aby założyć konto.')

	class Meta:
		model = Account
		fields = ['email', 'username', 'password1', 'password2']


	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" jest już zajęty.' % account)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError('Nazwa "%s" jest już zajęta.' % username)

class LoginForm(ModelForm):
	class Meta:
		model = Account
		fields = ['email', 'password']

class PostForm(ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'body', 'image']

class UserSettingsForm(ModelForm):
	email = forms.EmailField(required=False)
	username = forms.CharField(max_length=32 ,required=False)

	class Meta:
		model = Account
		fields = ['email', 'username']