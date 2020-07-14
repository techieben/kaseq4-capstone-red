from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django import forms
from user.models import CustomUser
from user.forms import CustomUserChangeForm
from recipe.models import Recipe


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
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return render(request, self.html, {'form': form})


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