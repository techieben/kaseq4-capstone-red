from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Author


class AuthorCreationForm(UserCreationForm):
    # display_name = forms.CharField(max_length=50)
    # followers = forms.ModelMultipleChoiceField(
    #     queryset=TwitterUser.objects.all())

    class Meta:
        model = Author
        fields = ('username', 'email', 'display_name')


class AuthorChangeForm(UserChangeForm):

    class Meta:
        model = Author
        fields = ('username', 'email')
