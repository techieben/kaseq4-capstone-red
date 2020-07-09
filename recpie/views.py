from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import RecpieItems, Author
from recpie.forms import AddRecpieForm, AddAuthorForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from recpie.forms import LoginForm


def index(request):
    data = RecpieItems.objects.all()
    author = Author.objects.all()
    return render(request, 'index.html', {'data': data, 'author': author})

def author(request, id):
    data = RecpieItems.objects.all()
    author = Author.objects.get(id=id)
    recpie = RecpieItems.objects.filter(author=author)
    meal_type = RecpieItems.objects.get(id=id)
    return render(request, 'author.html', {
        'data': data, 'author': author, 'recpie': recpie
    })

def recpie(request, id):
    recpie = RecpieItems.objects.all(id=id)
    return render(request, 'recpie.html', {'recpie': recpie})

@login_required
def add_recpie (request):
    html = "generic_form.html"
    form = AddRecpieForm()
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        author = RecpieItems.objects.create(
            title=data['title'],
            author=request.user.author,
            meal_option=data['meal_option'],
            description=data['description'],
            time_required=data['time_required'],
            instructions=data['instructions'],
            email=data['email'],
        )
        return HttpResponseRedirect(reverse('homepage'))
    return render(request, html, {'form': form})

@login_required
def add_author(request):
    html = "generic_form.html"
    form = AddAuthorForm()
    if request.method == "POST" and form.is_valid():
        form = AddAuthorForm(request.POST)
        data = form.cleaned_data
        new_user = User.objects.create_user(
            username=data['name'],
        )
        new_author = Author.objects.create(
            name=data['name'], bio=data['bio'], user=new_user)
        new_author.save()
    return render(request, html, {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )
    form = LoginForm()
    return render(request, 'generic_form.html', {'form': form})

def logout_view(request):
    if logout(request):
        return HttpResponseRedirect(reverse('homepage'))
    return render(request, 'index.html', {})

@login_required
def nutrition_label(request):
    # nutrition_information = RecpieItems.objects.all(id=id)
    return render(request, 'nutrition_label.html', {})
