from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from homepage.forms import HeaderForm
from homepage.models import Header
from django.contrib import messages
import os


def adminbase(request):
    headers = Header.objects.all()
    context = {
        'headers': headers
    }
    return render(request, 'admin_base.html', context)


def adminhome(request):
    template = loader.get_template('admin_home.html')
    return HttpResponse(template.render())


def manage_header(request):
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


def edit_header(request, pk):
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


def delete_header(request, pk):
    headers = Header.objects.get(id=pk)
    if len(headers.logo) > 0:
        os.remove(headers.logo.path)
    headers.delete()
    messages.success(request, "Header Deleted Successfully ")


def display_header_logo(request):
    header = Header.objects.all()
    return render(request, 'base.html', {'header_objects': header})
