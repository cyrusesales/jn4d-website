from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from homepage.forms import HeaderForm
from homepage.models import Header, Carousel
from django.contrib import messages
import os


def adminBase(request):
    headers = Header.objects.all()
    context = {
        'headers': headers
    }
    return render(request, 'admin_base.html', context)


def adminHome(request):
    template = loader.get_template('admin_home.html')
    return HttpResponse(template.render())


def manageHeader(request):
    headers = Header.objects.all()
    if request.method == 'POST':
        header = Header()
        header.menu_item1 = request.POST.get('menu_item1')
        header.menu_item2 = request.POST.get('menu_item2')
        header.menu_item3 = request.POST.get('menu_item3')
        header.menu_item4 = request.POST.get('menu_item4')

        if len(request.FILES) != 0:
            header.logo = request.FILES['logo']

        header.save()
        messages.success(
            request, "Header's logo and menu items are added successfully!")
        return redirect('/')
    context = {'headers': headers}
    return render(request, 'header_page.html', context)


def editHeader(request, pk):
    headers = Header.objects.get(id=pk)

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(headers.logo) > 0:
                os.remove(headers.logo.path)
            headers.logo = request.FILES['logo']
        headers.menu_item1 = request.POST.get('menu_item1')
        headers.menu_item2 = request.POST.get('menu_item2')
        headers.menu_item3 = request.POST.get('menu_item3')
        headers.menu_item4 = request.POST.get('menu_item4')
        headers.save()
        messages.success(request, "Header Updated Successfully")
    context = {'headers': headers}
    return render(request, 'edit_header.html', context)


def deleteHeader(request, pk):
    headers = Header.objects.get(id=pk)
    if len(headers.logo) > 0:
        os.remove(headers.logo.path)
    headers.delete()
    messages.success(request, "Header Deleted Successfully ")


def display_header_logo(request):
    header = Header.objects.all()
    return render(request, 'base.html', {'header_objects': header})


def manageCarousel(request):
    headers = Header.objects.all()
    carousels = Carousel.objects.all()
    context = {
        'carousels': carousels,
        'headers': headers
    }
    return render(request, 'manage_carousel.html', context)


def editCarousel(request, pk):
    carousels = Carousel.objects.get(id=pk)

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(carousels.image) > 0:
                os.remove(carousels.image.path)
        carousels.label = request.POST.get('label')
        carousels.caption = request.POST.get('caption')
        carousels.save()
        messages.success(request, "Carousel Updated Successfully")

    context = {
        'carousels': carousels
    }
    return redirect(request, 'edit_carousel.html', context)


def addCarousel(request):
    carousels = Carousel.objects.all()

    if request.method == "POST":
        carousel = Carousel()
        carousel.label = request.POST.get('label')
        carousel.caption = request.POST.get('caption')

        if len(request.FILES) != 0:
            carousel.image = request.FILES['image']

        carousel.save()
        messages.success(request, "New Slide Photo Saved Successfully")
        return redirect('manage-carousel')

    context = {
        'carousels': carousels
    }
    return render(request, 'add_carousel.html', context)
