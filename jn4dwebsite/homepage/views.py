from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from .models import Header, Carousel, Category, Product, ColorProduct, Placeholder, UserProfile
from django.contrib import messages
from django.template.exceptions import TemplateDoesNotExist
import re
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.


def base(request):
    headers = Header.objects.all()
    userpro = UserProfile.objects.all()
    context = {
        'headers': headers,
        'userpro': userpro,
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
        products = Product.objects.filter(category__id=pk).order_by('id')
        category = Category.objects.get(id=pk)
        placeholders = Placeholder.objects.all()
        context = {
            'headers': headers,
            'products': products,
            'category': category,
            'placeholders': placeholders,
        }
        return render(request, 'product_section.html', context)
    else:
        messages.warning(request, 'No Products Available.')
        return render('view-products')
    

def viewColorProducts(request, pk):
    if (Product.objects.filter(id=pk)):
        headers = Header.objects.all()
        colorProducts = ColorProduct.objects.filter(product__id=pk).order_by('id')
        product = Product.objects.get(id=pk)
        category = Category.objects.get(id=product.category.id)
        placeholders = Placeholder.objects.all()
        context = {
            'headers': headers,
            'colorProducts': colorProducts,
            'product': product,
            'category': category,
            'placeholders': placeholders,
        }
        return render(request, 'color_product_section.html', context)
    else:
        messages.warning(request, 'No Product Color Available.')
        return render(request, 'view-color-products')
    

def viewSpecifications(request, pk):
    # headers = Header.objects.all()

    # try:
    #     colorProducts = ColorProduct.objects.get(id=pk)
    # except ColorProduct.DoesNotExist:
    #     messages.warning(request, 'No Product Available')
    #     return redirect('view-color-products')

    # category = colorProducts.category
    # product = colorProducts.product

    # context = {
    #     'headers': headers,
    #     'colorProducts': colorProducts,
    #     'category': category,
    #     'product': product,
    # }
    # return render(request, 'product_specifications.html', context)
    if (ColorProduct.objects.filter(id=pk)):
        headers = Header.objects.all()
        colorProducts = ColorProduct.objects.get(id=pk)
        category = Category.objects.get(id=colorProducts.category.id)
        product = Product.objects.get(id=colorProducts.product.id)
        placeholders = Placeholder.objects.all()
        variations = ColorProduct.objects.filter(product__id=product.id)
        context = {
            'headers': headers,
            'colorProducts': colorProducts,
            'category': category,
            'product': product,
            'placeholders': placeholders,
            'variations': variations,
        }
        return render(request, 'product_specifications.html', context)
    else:
        messages.warning(request, 'No Product Available')
        return render('view-specifications')
    
def signUp(request):
    headers = Header.objects.all()
    # userprofile = UserProfile.objects.all()

    if request.method == "POST":
        # userprofile = UserProfile()
        username = request.POST.get('username')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        dateOfBirth = request.POST.get('dateOfBirth')
        phoneNumber = request.POST.get('full_phone')

        

        validator = EmailValidator()

        try:
            # Username validator
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exists!')
                return redirect('sign-up')
            
            # Email validatiom
            if UserProfile.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exists!')
                return redirect('sign-up')

            validator(email)

            # Password validation
            regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$%]).{12,16}$"
            
            if not re.match(regex, password):
                messages.warning(request, 
                    "Password must be 12-16 characters long and at least one uppercase, one lowercase, one number, and one symbol (@#$%).""")
                return redirect('sign-up')

            # Phone validation
            if not phoneNumber or not re.match(r'^\+\d{8,15}$', phoneNumber):
                messages.warning(request, "Invalid phone number")
                return redirect('sign-up')

             # Create User
            user = User.objects.create_user(
                username=username,
                password=password,
            )

            # Create user profile
            UserProfile.objects.create(
                user=user,
                firstName=firstName,
                lastName=lastName,
                email=email,
                dateOfBirth=dateOfBirth,
                phoneNumber=phoneNumber,
            )

            messages.success(request, "Sign Up Completed!")
            return redirect('sign-in')
                    
        except ValidationError:
            messages.warning(request, "Invalid Email Address")

        except Exception as e:
            messages.warning(request, f"Unexpected Error occured: {e}")

    context = {
        'headers': headers,
        # 'userprofile': userprofile,
    }
    return render(request, 'sign_up.html', context)

def signIn(request):
    headers = Header.objects.all()
    # userprofile = User.objects.all()

    if request.method == 'POST':
        # userprofile = UserProfile()
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('homepage')
            # messages.success(request, 'Succesfully Login')
        else:
            messages.warning(request, 'Invalid username or password')

    context = {
        'headers': headers,
        # 'userprofile': userprofile,
    }

    return render(request, 'sign_in.html', context)

def signOut(request):
    logout(request)
    messages.info(request, "Logged out successfully!")

    return redirect('homepage')


def viewUserProfile(request, pk):
    headers = Header.objects.all()
    userprofile = UserProfile.objects.get(user_id=pk)

    context = {
        'headers': headers,
        'userprofile': userprofile,
    }
    return render(request, 'view_userprofile.html', context)