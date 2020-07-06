from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import RecpieItems, Author
from recpie.forms import AddRecpieForm, AddAuthorForm


def index(request):
    data = RecpieItems.objects.all()
    author = Author.objects.all()
    return render(request, 'index.html', {'data': data, 'author': author})

def author(request, id):
    data = RecpieItems.objects.all()
    author = Author.objects.get(id=id)
    recpie = RecpieItems.objects.filter(author=author)
    return render(request, 'author.html', {
        'data': data, 'author': author, 'recpie': recpie
    })

def recpie(request, id):
    recpie = RecpieItems.objects.all(id=id)
    return render(request, 'recpie.html', {'recpie': recpie})

def add_recpie (request):
    html = "generic_form.html"
    form = AddRecpieForm()
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        author = RecpieItems.objects.create(
            title=data['title'],
            author=request.user.author,
            description=data['description'],
            time_required=data['time_required'],
            instructions=data['instructions'],
        )
        return HttpResponseRedirect(reverse('homepage'))
    return render(request, html, {'form': form})

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
