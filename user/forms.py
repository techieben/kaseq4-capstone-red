from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from user.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    password = None
    bio = forms.CharField(required=False, widget=forms.Textarea)

    # used for how to do  __init__
    # https://stackoverflow.com/questions/23580771/overwrite-django-allauth-form-field
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if type(field.widget) in (forms.TextInput, forms.DateInput):
                    field.widget = forms.TextInput(attrs={'placeholder': field.label})

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'bio')
        exclude = ('email',)


# For extra fields in Sign up form if wanted also uncomment ACCOUNT_SIGNUP_FORM_CLASS in settings.py
# For a completely cusotm Sign up form add to ACCOUNT_FORMS in settings. py instead

# class SignupForm(forms.Form):
#     display_name = forms.CharField(max_length=50)
#
#     def signup(self, request, user):
#         user.display_name = self.cleaned_data['display_name']
#         user.save()
