from django import forms
from .models import Recipe
import datetime

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'image', 'tags', 'ingredients', 'instructions',
            'servings', 'time_prep', 'time_cook', 'time_additional'
        ]

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    date = forms.DateField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
