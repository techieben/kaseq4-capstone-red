from recipe.models import Recipe
from review.models import Review
from django.shortcuts import render
from django.db.models import Avg, Func


def IndexView(request):
    class Round(Func):
        function = 'ROUND'
        arity = 2

    html = 'index.html'
    recipes = Recipe.objects.all()
    avg_rating = []
    for recipe in recipes:
        avg_rating.append(Review.objects.filter(
            id=recipe.id).aggregate(avg_rate=Round(Avg('rating'), 1)))
    return render(request, html, {
        'recipes': recipes,
        'avg_rating': avg_rating
    })
