from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Author
from recipe.models import Recipe
from .forms import AuthorCreationForm
from django.views.generic import View


def AuthorView(request, id):
    html = "author.html"
    author = Author.objects.get(id=id)
    recipes = Recipe.objects.filter(author=author).order_by('-date')
    return render(request, html, {'author': author, 'recipes': recipes})

# https://stackoverflow.com/questions/3222549/
# how-to-automatically-login-a-user-after-registration-in-django


class RegisterView(View):
    html = "form.html"

    def get(self, request):
        form = AuthorCreationForm()
        return render(request, self.html, {'form': form})

    def post(self, request):
        form = AuthorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_author = authenticate(username=form.cleaned_data['username'],
                                      password=form.cleaned_data['password1'],
                                      )
            login(request, new_author)
            return HttpResponseRedirect(reverse('index'))
        return render(request, self.html, {'form': form})


@login_required
def FollowView(request, id):
    request.user.following.add(Author.objects.get(id=id))
    return HttpResponseRedirect(reverse('author', args=(id,)))


@login_required
def UnfollowView(request, id):
    request.user.following.remove(Author.objects.get(id=id))
    return HttpResponseRedirect(reverse('author', args=(id,)))
