from django import forms
from review.models import Review


class AddReviewForm(forms.ModelForm):
    author = forms.CharField(widget=forms.HiddenInput)
    recipe = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Review
        fields = ['title', 'rating', 'content', 'author', 'recipe']
