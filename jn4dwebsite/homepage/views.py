from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Header, Carousel

# Create your views here.


def base(request):
    headers = Header.objects.all()
    context = {
        'headers': headers
    }
    return render(request, 'base.html', context)


def homepage(request):
    # template = loader.get_template('index.html')
    # return HttpResponse(template.render())
    headers = Header.objects.all()
    carousels = Carousel.objects.all()
    context = {
        'carousels': carousels,
        'headers': headers,
    }
    return render(request, 'index.html', context)


def carousel(request):
    carousels = Carousel.objects.all()
    headers = Header.objects.all()
    context = {
        'carousels': carousels,
        'headers': headers,
    }
    return render(request, 'slider_section.html', context)
