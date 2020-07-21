from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'image', 'tags', 'ingredients', 'instructions',
            'servings', 'time_prep', 'time_cook', 'time_additional'
        ]
