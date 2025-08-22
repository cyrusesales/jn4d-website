from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from homepage.forms import HeaderForm


def adminhome(request):
    template = loader.get_template('admin_home.html')
    return HttpResponse(template.render())


def manage_header(request):
    if request.method == 'POST':
        form = HeaderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return redirect('success_page') # Redirect to a success
    else:
        form = HeaderForm()
    return render(request, 'header_page.html', {'form': form})
