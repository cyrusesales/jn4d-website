from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Header

# Create your views here.


def homepage(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def display_header_logo(request):
    logo = Header.objects.all()
    return render(request, 'base.html', {'logo': logo})
