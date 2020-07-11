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
    
class SignupForm(forms.Form):
    display_name = forms.CharField(max_length=50)
    bio = forms.CharField(max_length=450, widget=forms.Textarea)
    
    def signup(self, request, user):
        user.display_name = self.cleaned_data['display_name']
        user.bio = self.cleaned_data['bio']
        user.save()