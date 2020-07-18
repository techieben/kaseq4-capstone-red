from recipe.models import Recipe
from django.shortcuts import render


def IndexView(request):
    html = 'index.html'
    recipes = Recipe.objects.all()
    return render(request, html, {'recipes': recipes})


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)
