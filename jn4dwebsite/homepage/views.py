from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Header, Carousel, Category

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
    categories = Category.objects.all()

    context = {
        'carousels': carousels,
        'headers': headers,
        'categories': categories,
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

def category(request):
    categories = Category.objects.all()
    headers = Header.objects.all()

    context = {
        'categories': categories,
        'headers': headers,
    }
    return render(request, 'category_section.html', context)
