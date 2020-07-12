from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from user.models import CustomUser
from recipe.models import Recipe


# Create your views here.
def ProfileView(request, username):
    html = "profile.html"
    profile = CustomUser.objects.get(username=username)
    recipes = Recipe.objects.filter(author=profile).order_by('-date_created')
    return render(request, html, {'profile': profile, 'recipes': recipes})

def ProfileEditView(request):
    html = "profile_edit.html"
    profile = request.user
    


@login_required
def FollowView(request, username):
    request.user.following.add(CustomUser.objects.get(username=username))
    CustomUser.objects.get(username=username).followers.add(request.user)
    return HttpResponseRedirect(reverse('profile', args=(username,)))


@login_required
def UnfollowView(request, username):
    request.user.following.remove(CustomUser.objects.get(username=username))
    CustomUser.objects.get(username=username).followers.remove(request.user)
    return HttpResponseRedirect(reverse('profile', args=(username,)))