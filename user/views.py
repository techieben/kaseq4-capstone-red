from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
# from django import forms
from user.models import CustomUser
from user.forms import CustomUserChangeForm
from recipe.models import Recipe
from notification.models import Notification


# Create your views here.
def ProfileView(request, username):
    html = "profile.html"
    profile = CustomUser.objects.get(username=username)
    recipes = Recipe.objects.filter(author=profile).order_by('-date_created')
    return render(request, html, {'profile': profile, 'recipes': recipes})


class ProfileEditView(View):
    html = "profile_edit.html"

    def get(self, request):
        form = CustomUserChangeForm(instance=request.user)
        return render(request, 'profile_edit.html', {'form': form})

    def post(self, request):
        html = "profile.html"
        recipes = Recipe.objects.filter(
            author=request.user).order_by('-date_created')
        form = CustomUserChangeForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, html, {'profile': request.user, 'recipes': recipes})
        # return HttpResponseRedirect(reverse('profile', args=(request.user.username,)))
        return render(request, self.html, {'form': form})


@login_required
def FollowView(request, username):
    request.user.following.add(CustomUser.objects.get(username=username))
    Notification.objects.create(
        user_to=CustomUser.objects.get(username=username),
        user_from=request.user,
        text=str(request.user) + " is following you."
    )
    return HttpResponseRedirect(reverse('profile', args=(username,)))


@login_required
def UnfollowView(request, username):
    request.user.following.remove(CustomUser.objects.get(username=username))
    Notification.objects.create(
        user_to=CustomUser.objects.get(username=username),
        user_from=request.user,
        text=str(request.user) + " has unfollowed you."
    )
    return HttpResponseRedirect(reverse('profile', args=(username,)))
