from recipe.models import Recipe
# from django.views.generic import ListView
from django.shortcuts import render


def SearchView(request):
    html = 'search.html'
    # recipes = Recipe.objects.all().order_by('-date_created')[:10]
    recipes = Recipe.objects.all()
    return render(request, html, {'recipes': recipes})
