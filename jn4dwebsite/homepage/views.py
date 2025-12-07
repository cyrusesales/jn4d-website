from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Header, Carousel, Category, Product, ColorProduct
from django.contrib import messages

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


def viewProducts(request, pk):
    if (Category.objects.filter(id=pk)):
        headers = Header.objects.all()
        products = Product.objects.filter(category__id=pk)
        category = Category.objects.get(id=pk)
        context = {
            'headers': headers,
            'products': products,
            'category': category,
        }
        return render(request, 'product_section.html', context)
    else:
        messages.warning(request, 'No Products Available.')
        return render('view-products')
    

def viewColorProducts(request, pk):
    if (Product.objects.filter(id=pk)):
        headers = Header.objects.all()
        colorProducts = ColorProduct.objects.filter(product__id=pk)
        product = Product.objects.get(id=pk)
        category = Category.objects.get(id=product.category.id)
        context = {
            'headers': headers,
            'colorProducts': colorProducts,
            'product': product,
            'category': category,
        }
        return render(request, 'color_product_section.html', context)
    else:
        messages.warning(request, 'No Product Color Available.')
        return render('view-color-products')