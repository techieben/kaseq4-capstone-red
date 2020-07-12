from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from user.models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'display_name')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


# For extra fields in Sign up form if wanted also uncomment in settings.py
# For a completely cusotm Sign up form add to ACCOUNT_FORMS in settings. py instead

# class SignupForm(forms.Form):
#     display_name = forms.CharField(max_length=50)
# 
#     def signup(self, request, user):
#         user.display_name = self.cleaned_data['display_name']
#         user.save()