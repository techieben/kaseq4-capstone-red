from recipe.models import Recipe
from django.shortcuts import render


def IndexView(request):
    html = 'index.html'
    recipes = Recipe.objects.all()
    return render(request, html, {'recipes': recipes})
