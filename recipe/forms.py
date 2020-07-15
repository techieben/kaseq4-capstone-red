from django import forms
from .models import Recipe, RecipeCard


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'tags', 'ingredients', 'instructions',
            'servings', 'time_prep', 'time_cook', 'time_additional'
        ]

class RecipeCard(forms.ModelForm):
    class Meta:
        model = RecipeCard
        fields = ['title', 'recipe_picture']
