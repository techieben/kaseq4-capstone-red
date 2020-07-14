from django.shortcuts import render, reverse, HttpResponseRedirect
from .models import Recipe, RecipeCard
from .forms import RecipeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


def RecipeView(request, title):
    html = "recipe.html"
    recipe = Recipe.objects.get(title=title)
    return render(request, html, {'recipe': recipe, })

def RecipeCard(request, form):
    html = "recipe_card.html"
    form = RecipeForm()
    if form.is_valid():
        data = form.cleaned_data
        recipe = Recipe.objects.create(
            title = Recipe.objects.get({'form': form})
            recipe_picture = Recipe.objects.get({'form': form})
            )
        return HttpResponseRedirect(reverse('recipe', args=(recipe.title,)))
    return render(request, html, {'title': title, 'recipe_picture': recipe_picture})

class RecipeAddView(LoginRequiredMixin, View):

    def get(self, request):
        html = "form.html"
        form = RecipeForm()
        return render(request, html, {"form": form})

    def post(self, request):
        html = "form.html"
        form = RecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            recipe = Recipe.objects.create(
                author=request.user,
                title=data['title'],
                description=data['description'],
                tags=data['tags'],
                ingredients=data['ingredients'],
                instructions=data['instructions'],
                servings=data['servings'],
                time_prep=data['time_prep'],
                time_cook=data['time_cook'],
                time_additional=data['time_additional'],
            )
            return HttpResponseRedirect(reverse('recipe', args=(recipe.title,)))
        return render(request, html, {"form": form})
