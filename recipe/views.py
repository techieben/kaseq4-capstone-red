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
import requests


class RecipeView(View):
    def get(self, request, title):
        class Round(Func):
            function = 'ROUND'
            arity = 2

        html = "recipe.html"
        recipe = Recipe.objects.get(title=title)
        plain_prep = recipe.plain_time(recipe.time_prep)
        plain_cook = recipe.plain_time(recipe.time_cook)
        plain_additional = recipe.plain_time(recipe.time_additional)
        avg_rating = Review.objects.filter(
            recipe=recipe.id).aggregate(avg_rate=Round(Avg('rating'), 1))
        reviews = Review.objects.filter(recipe=recipe)
        form = AddReviewForm(initial={'recipe': Recipe.objects.get(
            title=title), 'author': request.user})
        return render(request, html, {
            'recipe': recipe,
            'plain_prep': plain_prep,
            'plain_cook': plain_cook,
            'plain_additional': plain_additional,
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
                text=str(request.user) + " left a review on your recipe " +
                str(recipe.title) + "."
            )
            form = AddReviewForm(initial={'recipe': Recipe.objects.get(
                title=title), 'author': request.user})

        return render(request, html, {
            'recipe': recipe,
            'avg_rating': avg_rating['avg_rate'],
            'reviews': reviews,
            'form': form
        })


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
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            recipe = Recipe.objects.create(
                author=request.user,
                title=data['title'],
                description=data['description'],
                image=data['image'],
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
                    text=str(request.user) + " posted a new recipe  " +
                    str(recipe.title) + "."
                )
            return HttpResponseRedirect(reverse('recipe',
                                                args=(recipe.title,)))
        return render(request, html, {"form": form})


@login_required
def RecipeEditView(request, title):
    recipe = get_object_or_404(Recipe, title=title)
    if request.user == recipe.author or request.user.is_superuser:
        if request.method == 'POST':
            form = RecipeForm(request.POST, request.FILES, instance=recipe)
            if form.is_valid():
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
            text=str(request.user) + " added " +
            str(recipe.title) + " to their favorites."
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
            text=str(request.user) + " removed " +
            str(recipe.title) + " from their favorites."
        )
    return HttpResponseRedirect(reverse('recipe', args=(title,)))


def RecipeNutritionView(request, title):
    html = 'recipe_nutrition.html'
    recipe = Recipe.objects.get(title=title)
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        'x-app-id': '737e78f4',
        'x-app-key': 'b33863a33f08cb00df2a437da6f050e9',
        'x-remote-user-id': '0',
        'Content-Type': 'application/json'
    }
    payload = "{\"query\": \"" + ' and '.join(recipe.ingredients) + "\"}"
    r = requests.request("POST", url, headers=headers, data=payload)
    data = r.json()
    calories = 0
    total_fat = 0
    saturated_fat = 0
    cholesterol = 0
    sodium = 0
    total_carbohydrate = 0
    dietary_fiber = 0
    sugars = 0
    protein = 0
    potassium = 0
    vitamin_a = 0
    vitamin_c = 0
    calcium = 0
    trans_fat = 0
    if r.status_code == requests.codes.ok:
        api_response = '200'
        for food in data['foods']:
            calories += food['nf_calories']
            total_fat += food['nf_total_fat']
            saturated_fat += food['nf_saturated_fat']
            cholesterol += food['nf_cholesterol']
            sodium += food['nf_sodium']
            total_carbohydrate += food['nf_total_carbohydrate']
            dietary_fiber += food['nf_dietary_fiber']
            sugars += food['nf_sugars']
            protein += food['nf_protein']
            potassium += food['nf_potassium']
            for obj in food['full_nutrients']:
                if obj['attr_id'] == 301:
                    calcium += obj['value']
                elif obj['attr_id'] == 401:
                    vitamin_c += obj['value']
                elif obj['attr_id'] == 320:
                    vitamin_a += obj['value']
                elif obj['attr_id'] == 605:
                    trans_fat += obj['value']
        return render(request, html, {
            'api_response': api_response,
            'calories': round(calories, 2),
            'total_fat': round(total_fat, 2),
            'saturated_fat': round(saturated_fat, 2),
            'cholesterol': round(cholesterol, 2),
            'sodium': round(sodium, 2),
            'total_carbohydrate': round(total_carbohydrate, 2),
            'dietary_fiber': round(dietary_fiber, 2),
            'sugars': round(sugars, 2),
            'protein': round(protein, 2),
            'potassium': round(potassium, 2),
            'vitamin_a': round(vitamin_a, 2),
            'vitamin_c': round(vitamin_c, 2),
            'trans_fat': round(trans_fat, 2),
            'calcium': round(calcium, 2)
        })
    else:
        api_response = '400'
        return render(request, html, {
            'api_response': api_response,
            'calories': round(calories, 2),
            'total_fat': round(total_fat, 2),
            'saturated_fat': round(saturated_fat, 2),
            'cholesterol': round(cholesterol, 2),
            'sodium': round(sodium, 2),
            'total_carbohydrate': round(total_carbohydrate, 2),
            'dietary_fiber': round(dietary_fiber, 2),
            'sugars': round(sugars, 2),
            'protein': round(protein, 2),
            'potassium': round(potassium, 2),
            'vitamin_a': round(vitamin_a, 2),
            'vitamin_c': round(vitamin_c, 2),
            'trans_fat': round(trans_fat, 2),
            'calcium': round(calcium, 2)
        })


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)
