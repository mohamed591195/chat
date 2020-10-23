from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

User = get_user_model()


class UserRegisterationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'image']


class UserModificationForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'
