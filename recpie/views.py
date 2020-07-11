from django.shortcuts import render
from user.models import CustomUser


def index(request):
    # breakpoint()
    return render(request, 'index.html')