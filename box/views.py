from recipe.models import Recipe
from django.views.generic import ListView


class IndexView(ListView):
    template_name = 'index.html'
    model = Recipe
    queryset = Recipe.objects.all().order_by('-date')[:20]
