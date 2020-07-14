from recipe.models import Recipe
# from django.views.generic import ListView
from django.shortcuts import render


# class IndexView(ListView):
#     template_name = 'index.html'
#     model = Recipe
#     queryset = Recipe.objects.all().order_by('-date_created')[:20]

def IndexView(request):
    html = 'index.html'
    recipes = Recipe.objects.all().order_by('-date_created')[:10]
    return render(request, html, {'recipes': recipes})
