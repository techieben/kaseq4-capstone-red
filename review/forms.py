from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from review.models import Review
from recipe.models import Recipe
from user.models import CustomUser


class AddReviewForm(forms.ModelForm):
    queryset_user = CustomUser.objects.all()
    queryset_recipe = Recipe.objects.all()
    author = forms.ModelChoiceField(
        queryset=queryset_user, widget=forms.HiddenInput)
    recipe = forms.ModelChoiceField(
        queryset=queryset_recipe, widget=forms.HiddenInput)

    class Meta:
        model = Review
        fields = ['title', 'rating', 'content', 'author', 'recipe']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "You cannot write a second review, please edit your existing review.",
            }
        }


class EditReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'rating', 'content']
