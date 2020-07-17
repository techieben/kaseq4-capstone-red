from django.shortcuts import (render,
                              reverse,
                              HttpResponseRedirect,
                              get_object_or_404)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe
from .forms import RecipeForm
from review.models import Review
from notification.models import Notification
from review.forms import AddReviewForm
from django.views.generic import View
from django.db.models import Avg, Func


class RecipeView(View):
    def get(self, request, title):
        class Round(Func):
            function = 'ROUND'
            arity = 2

        html = "recipe.html"
        recipe = Recipe.objects.get(title=title)
        avg_rating = Review.objects.filter(
            recipe=recipe.id).aggregate(avg_rate=Round(Avg('rating'), 1))
        reviews = Review.objects.filter(recipe=recipe)
        form = AddReviewForm(initial={'recipe': Recipe.objects.get(
            title=title), 'author': request.user})
        return render(request, html, {
            'recipe': recipe,
            'avg_rating': avg_rating['avg_rate'],
            'reviews': reviews,
            'form': form
        })

    def post(self, request, title):
        class Round(Func):
            function = 'ROUND'
            arity = 2
        html = 'recipe.html'
        recipe = Recipe.objects.get(title=title)
        avg_rating = Review.objects.filter(
            recipe=recipe.id).aggregate(avg_rate=Round(Avg('rating'), 1))
        reviews = Review.objects.filter(recipe=recipe.id)
        form = AddReviewForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            new_review = Review.objects.create(
                title=data['title'],
                rating=data['rating'],
                content=data['content'],
                author=request.user,
                recipe=recipe
            )
            new_review.save()
            Notification.objects.create(
                user_to=recipe.author,
                user_from=request.user,
                recipe=recipe,
                review=new_review,
                text=str(request.user) + " left a review on your recipe " + str(recipe.title) + "."
            )
            form = AddReviewForm(initial={'recipe': Recipe.objects.get(
                title=title), 'author': request.user})

        return render(request, html, {
            'recipe': recipe,
            'avg_rating': avg_rating['avg_rate'],
            'reviews': reviews,
            'form': form
        })


def RecipeCard(request):
    html = "recipe_card.html"
    form = RecipeForm()
    if form.is_valid():
        data = form.cleaned_data
        recipe = Recipe.objects.create(
            title=data['title'],
            recipe_picture=data['recipe_picture']
        )
        recipe.save()
        return HttpResponseRedirect(reverse('recipe', args=(recipe.title,)))
    return render(request, html, {'form': form})


def FavoriteListView(request, sort):
    html = 'favorites.html'
    print(request)
    print("sort: ", sort)
    if sort == 'title':
        recipes = request.user.favorites.order_by('title')
    elif sort == 'time_prep':
        recipes = request.user.favorites.order_by('time_prep')
    elif sort == 'date_old':
        recipes = request.user.favorites.order_by('date_created')
    else:
        recipes = request.user.favorites.order_by('-date_created')
    print(recipes)
    return render(request, html, {'recipes': recipes})


class RecipeAddView(LoginRequiredMixin, View):

    def get(self, request):
        for follower in request.user.followed_by.all():
            print(follower.username)
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
            for follower in request.user.followed_by.all():
                Notification.objects.create(
                    user_to=follower,
                    user_from=request.user,
                    recipe=recipe,
                    text=str(request.user) + " posted a new recipe  " + str(recipe.title) + "."
                )
                # for user in request.user.following
            return HttpResponseRedirect(reverse('recipe',
                                                args=(recipe.title,)))
        return render(request, html, {"form": form})


@login_required
def RecipeEditView(request, title):
    recipe = get_object_or_404(Recipe, title=title)
    if request.user == recipe.author or request.user.is_superuser:
        if request.method == 'POST':
            form = RecipeForm(request.POST, instance=recipe)
            form.save()
            return HttpResponseRedirect(reverse('recipe', args=(title,)))

        form = RecipeForm(instance=recipe)
        return render(request, "form.html", {'form': form})
    return HttpResponseRedirect(reverse('recipe', args=(title,)))


@login_required
def FavoriteView(request, title):
    Recipe.objects.get(title=title).favorited_by.add(request.user)
    recipe = Recipe.objects.get(title=title)
    if recipe.author != request.user:
        Notification.objects.create(
            user_to=recipe.author,
            user_from=request.user,
            recipe=recipe,
            text=str(request.user) + " added " + str(recipe.title) + " to their favorites."
        )
    return HttpResponseRedirect(reverse('recipe', args=(title,)))


@login_required
def UnfavoriteView(request, title):
    Recipe.objects.get(title=title).favorited_by.remove(request.user)
    recipe = Recipe.objects.get(title=title)
    if recipe.author != request.user:
        Notification.objects.create(
            user_to=recipe.author,
            user_from=request.user,
            recipe=recipe,
            text=str(request.user) + " removed " + str(recipe.title) + " from their favorites."
        )
    return HttpResponseRedirect(reverse('recipe', args=(title,)))


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)
