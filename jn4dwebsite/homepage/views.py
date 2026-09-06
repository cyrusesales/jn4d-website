from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from .models import Header, Carousel, Category, Product, Item, Placeholder, UserProfile, SizeTerm, Cart, User, SavedAddress, Order, Voucher, Wishlist
from django.contrib import messages
from django.template.exceptions import TemplateDoesNotExist
import re
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_POST
import requests
from django_countries import countries
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from django.db.models import OuterRef, Subquery
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from itertools import groupby
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
    

def viewItems(request, pk):
    if (Product.objects.filter(id=pk)):
        headers = Header.objects.all()
        items = Item.objects.filter(product__id=pk).order_by('id')
        product = Product.objects.get(id=pk)
        category = Category.objects.get(id=product.category.id)
        placeholders = Placeholder.objects.all()
        wishlist = set(Wishlist.objects.filter(user_id=request.user.id).values_list('item_id', flat=True))

        context = {
            'headers': headers,
            'items': items,
            'product': product,
            'category': category,
            'placeholders': placeholders,
            'wishlist': wishlist,
        }
        return render(request, 'item_section.html', context)
    else:
        messages.warning(request, 'No Product Color Available.')
        return render(request, 'view-items')
    

def viewSpecifications(request, pk):
    # headers = Header.objects.all()

    # try:
    #     colorProducts = ColorProduct.objects.get(id=pk)
    # except ColorProduct.DoesNotExist:
    #     messages.warning(request, 'No Product Available')
    #     return redirect('view-items')

    # category = colorProducts.category
    # product = colorProducts.product

    # context = {
    #     'headers': headers,
    #     'colorProducts': colorProducts,
    #     'category': category,
    #     'product': product,
    # }
    # return render(request, 'product_specifications.html', context)
    if (Item.objects.filter(id=pk)):
        headers = Header.objects.all()
        items = Item.objects.get(id=pk)
        category = Category.objects.get(id=items.category.id)
        product = Product.objects.get(id=items.product.id)
        placeholders = Placeholder.objects.all()
        variations = Item.objects.filter(product__id=product.id)
        sizeTerm = SizeTerm.objects.filter(productSize_id=items.size)
        
        context = {
            'headers': headers,
            'items': items,
            'category': category,
            'product': product,
            'placeholders': placeholders,
            'variations': variations,
            'sizeTerm': sizeTerm,
        }
        return render(request, 'product_specifications.html', context)
    else:
        messages.warning(request, 'No Product Available')
        return render('view-specifications')
    

def addToCart(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.user.id)
        item = get_object_or_404(Item, id=pk)
        selected_size = request.POST.get('selected_size')
        quantity = int(request.POST.get('quantity',1))

        # check if item already exist in cart
        cart_item = Cart.objects.filter(
            item=item,
            size=selected_size,
            status='cart',
        ).first()

        if cart_item:
            # update quantity
            cart_item.quantity += quantity
            cart_item.save()
        else:
            # create new cart item
            Cart.objects.create(
                user=user,
                item=item,
                size=selected_size,
                quantity=quantity,
            )
    return redirect ('view-specifications', item.id)


def viewCart(request, pk):
    headers = Header.objects.all()
    placeholders = Placeholder.objects.all()
    cart_items = Cart.objects.filter(user_id=pk).order_by('created_at').filter(status='cart')
    shippingFee = Decimal('50.00')
    total = sum(cart.total_price() for cart in cart_items) + shippingFee
    order_value = sum(cart.original_price() for cart in cart_items)
    discount = sum(cart.discount_price() for cart in cart_items)

    context = {
        'headers': headers,
        'cart_items': cart_items,
        'total': total,
        'order_value': order_value,
        'discount': discount,
        'shippingFee': shippingFee,
        'placeholders': placeholders,
    }
    return render(request, "add_to_cart.html", context)

def viewCheckout(request, pk):
    headers = Header.objects.all()
    userprofile = UserProfile.objects.get(user_id=pk)
    cart_items = Cart.objects.filter(user_id=pk).order_by('created_at').filter(status='cart')
    
    # voucher = Voucher.objects.all()
    applied_codes = request.session.get('applied_vouchers', [])
    active_vouchers = Voucher.objects.filter(code__in=applied_codes, status='active')
    voucher_total_discount = sum(v.amount for v in active_vouchers)
    shippingFee = Decimal('50.00')

    order_value = sum(cart.original_price() for cart in cart_items)
    discount = sum(cart.discount_price()  for cart in cart_items)
    total = sum(cart.total_price()  for cart in cart_items) - voucher_total_discount + shippingFee
    

    if request.method == "POST":
        user = get_object_or_404(User, id=request.user.id)
        email = request.POST.get("email")
        country = request.POST.get("country")
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        address = request.POST.get("address")
        district = request.POST.get("district")
        postalcode = request.POST.get("postalcode")
        city = request.POST.get("city")
        province = request.POST.get("province")
        phone = request.POST.get("phone")

        save_address = request.POST.get("save_address")
        payment_method = request.POST.get("payment_method")

        #save address only if checkbox is checked
        if save_address:
            SavedAddress.objects.create(
                user=user,
                email=email,
                country=country,
                firstName=firstName,
                lastName=lastName,
                address=address,
                district=district,
                postalcode=postalcode,
                city=city,
                province=province,
                phone=phone,
                payment_method=payment_method,
                
            )

        #Create Order
        Order.objects.create(
            user=user,
            email=email,
            country=country,
            firstName=firstName,
            lastName=lastName,
            address=address,
            district=district,
            postalcode=postalcode,
            city=city,
            province=province,
            phone=phone,
            payment_method=payment_method,
            value=order_value,
            discount=discount,
            voucher=voucher_total_discount,
            shippingFee=shippingFee,
            total=total,
        )

        for v in active_vouchers:
            v.user = user
            v.status = 'inactive'
            v.save()

        new_order = Order.objects.latest('created_at')
        for cart in cart_items:
            if new_order.payment_method == 'Credit or Debit Card':
                cart.status = 'To ship'
            else:
                cart.status = 'To pay'
            cart.order_id = new_order.id
            cart.save()
            Wishlist.objects.filter(user_id=pk, item_id=cart.item_id).delete()

        applied_codes = request.session.get('applied_vouchers', [])
        if 'applied_vouchers' in request.session:
            del request.session['applied_vouchers']

        #Card details if card is selected
        if payment_method == 'card':
            cardname = request.POST.get("cardname")
            cardnumber = request.POST.get("cardnumber")
            expirydate = request.POST.get("expirydate")
            securitycode = request.POST.get("securitycode")

            print(cardname)
            print(cardnumber)
            print(expirydate)
            print(securitycode)

        return redirect("order-status-page", request.user.id)

    

    context = {
        'headers': headers,
        'cart_items': cart_items,
        'total': total,
        'order_value': order_value,
        'discount': discount,
        'countries': countries,
        'userprofile': userprofile,
        'active_vouchers': active_vouchers,
        'voucher_total_discount': voucher_total_discount,
        'shippingFee': shippingFee,
    }
    return render(request, "checkout.html", context)

def orderStatusPage(request, pk):
    headers = Header.objects.all()
    userprofile = UserProfile.objects.get(user_id=pk)
    latest_order = Order.objects.filter(user_id=pk).latest('created_at')
    cart_items = Cart.objects.filter(order_id=latest_order.id)
    # voucher = Voucher.objects.all()
    applied_codes = request.session.get('applied_vouchers', [])
    active_vouchers = Voucher.objects.filter(code__in=applied_codes, status='active')
    voucher_total_discount = sum(v.amount for v in active_vouchers)
    shippingFee = Decimal('50.00')

    order_value = sum(cart.original_price() for cart in cart_items)
    discount = sum(cart.discount_price()  for cart in cart_items)
    total = sum(cart.total_price()  for cart in cart_items) - voucher_total_discount + shippingFee

    context = {
        'headers': headers,
        'userprofile': userprofile,
        'latest_order': latest_order,
        'cart_items': cart_items,
        'order_value': order_value,
        'discount': discount,
        'total': total,
        'shippingFee': shippingFee,
    }

    return render(request, "order_status_page.html", context)


def manageVoucher(request, pk):
    if request.method == "POST":
        search_code = request.POST.get('discountcode', '').strip()

        try:
            voucher = Voucher.objects.get(code=search_code)

            if voucher.is_valid():
                # Initialize the voucher list in session if it doesn't exist
                if 'applied_vouchers' not in request.session:
                    request.session['applied_vouchers'] = []

                # Fetch current list
                vouchers_in_session = request.session['applied_vouchers']

                # Prevent adding the exact same voucher twice
                if search_code not in vouchers_in_session and voucher.status == 'active':
                    vouchers_in_session.append(search_code)
                    request.session['applied_vouchers'] = vouchers_in_session # svae back to session
                    messages.success(request,f"Voucher {search_code} applied successfully!")
                # elif voucher.status == 'inactive':
                #     messages.warning(request, "This voucher is not active or already used.")    
                else:
                    messages.warning(request, "This voucher is already applied.")    

            else:
                messages.error(request, "This voucher has expired or is valid.")

        except Voucher.DoesNotExist:
            messages.error(request, "Voucher code does not exist")
        # if voucher_code:
        #     # user = UserProfile.objects.get(user_id=pk)
        #     voucher = Voucher.objects.get(code=search_code)
        #     voucher.user_id = pk
        #     messages.success(request, f"This { search_code } code exist in {voucher.user.username } amount is ₱{ voucher.amount }")
        # else:
        #     messages.warning(request, f"This voucher code { search_code } does not exist!")        
            
        # userprofile = UserProfile.objects.get(user_id=pk)
        # userprofile.status = status
        # userprofile.save()
    return redirect("checkout", pk)

@require_POST
def updateQuantity(request, pk):
    cart_item = get_object_or_404(Cart, id=pk, user=request.user, status='cart')
    action = request.POST.get('action') # 'increase' or 'decrease'

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            messages.info(request, "Item removed from cart.")
            return redirect('view-cart', request.user.id)
    return redirect('view-cart', request.user.id)
    
@require_POST
def removeItem(request, pk):
    cart_item = get_object_or_404(Cart, id=pk, user=request.user, status='cart')
    cart_item.delete()
    return redirect('view-cart', request.user.id)

def addToWishlist(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.user.id)
        item = get_object_or_404(Item, id=pk)

        wish_item = Wishlist.objects.filter(
            item=item,
            status='wishlist',
        ).first()

        if wish_item:
            wish_item.save()
        else:
            Wishlist.objects.create(
                user=user,
                item=item,
                status='wishlist',
            )
    return redirect('view-items', item.product_id)

def viewWishlist(request, pk):
    headers = Header.objects.all()
    placeholders = Placeholder.objects.all()
    wish_items = Wishlist.objects.filter(user_id=pk, status='wishlist').order_by('created_at')
    context = {
        'headers': headers,
        'placeholders': placeholders,
        'wish_items': wish_items,
    }
    return render(request, "view_wishlist.html", context)

def removeToWishlist(request, pk):
    wish_item = get_object_or_404(Wishlist, id=pk, user=request.user, status='wishlist')
    wish_item.delete()
    return redirect('view-wishlist', request.user.id)

def viewMyOrders(request, pk):
    headers = Header.objects.all()
    placeholders = Placeholder.objects.all()
    #used in blank search bar
    all_orders = Cart.objects.filter(Q(status='ordered') | 
                                     Q(status='To pay') |
                                     Q(status='To ship'),
                                     user_id=pk).order_by('-order_id', 'status')
    #Group cart records by order_id
    grouped_orders = []

    # group_key = lambda x: (x['order_id'], x['status'])
    group_key = lambda x: (x.order_id, x.status)

    for (order_id, status), items in groupby(
        all_orders,
        key=group_key,
    ):
        grouped_orders.append({
            'order_id': order_id,
            'items': list(items),
            'status': status,
        })

    paginator = Paginator(grouped_orders, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # used in search bar
    keyword = request.GET.get('q', '').strip()
    carts = Cart.objects.filter(Q(status='ordered') | 
                                Q(status='To pay') |
                                Q(status='To ship'),
                                user_id=pk).order_by('-order_id', 'status')
    if keyword:
        carts = carts.filter(
            Q(size__icontains=keyword) |
            Q(item__itemName__icontains=keyword) 
        )
    #Group cart records by order_id
    grouped_orders_search = []

    group_key = lambda x: (x.order_id, x.status)

    for (order_id, status), items in groupby(
        carts,
        key=group_key,
    ):
        grouped_orders_search.append({
            'order_id': order_id,
            'items': list(items),
            'status': status,
        })

    
    paginator2 = Paginator(grouped_orders_search, 5)
    page_number2 = request.GET.get('page')
    page_obj_search = paginator2.get_page(page_number2)

    

    context = {
        'headers': headers,
        'placeholders': placeholders,
        'all_orders': all_orders,
        'keyword': keyword,
        'carts': carts,
        'page_obj': page_obj,
        'page_obj_search': page_obj_search,
    }
    return render(request, "view_my_orders.html", context)


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
            
            # Phone Number validatiom
            if UserProfile.objects.filter(phoneNumber=phoneNumber).exists():
                messages.warning(request, 'Phone number already exists!')
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

@login_required
def viewUserProfile(request, pk):
    headers = Header.objects.all()
    userprofile = UserProfile.objects.get(user_id=pk)

    context = {
        'headers': headers,
        'userprofile': userprofile,
    }
    return render(request, 'view_userprofile.html', context)

@login_required
def editUserProfile(request, pk):
    headers = Header.objects.all()
    user = User.objects.get(id=pk)
    userprofile = UserProfile.objects.get(user_id=pk)

    if request.method == 'POST':
        user.username = request.POST.get("username")
        userprofile.firstName = request.POST.get("firstName")
        userprofile.lastName = request.POST.get("lastName")
        userprofile.email = request.POST.get("email")
        userprofile.dateOfBirth = request.POST.get("dateOfBirth")
        userprofile.phoneNumber = request.POST.get("phoneNumber")

        # Username validator
        if User.objects.filter(username=user.username).exists():
            messages.warning(request, 'Username already exists!')
        # Email validatiom
        elif UserProfile.objects.filter(email=userprofile.email).exists():
            messages.warning(request, 'Email already exists!')
        # Phone Number validation
        elif UserProfile.objects.filter(phoneNumber=userprofile.phoneNumber).exists():
            messages.warning(request, 'Phone number already exists!')
        # Phone validation
        elif not userprofile.phoneNumber or not re.match(r'^\+\d{8,15}$', userprofile.phoneNumber):
            messages.warning(request, "Invalid phone number")
        else:
            user.save()
            userprofile.save()
            messages.success(request, "User Profile successfully update!")

    context = {
        'headers': headers,
        'user': user,
        'userprofile': userprofile,
    }
    return render(request, 'edit_userprofile.html', context)

@login_required
def changePassword(request, pk):
    headers = Header.objects.all()
    user = User.objects.get(id=pk)

    if request.method == 'POST':
        old_pwd = request.POST.get("password")
        new_pwd1 = request.POST.get("new_password1")
        new_pwd2 = request.POST.get("new_password2")

        # Password validation
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$%]).{12,16}$"
        if not re.match(regex, new_pwd1):
            messages.error(request, 
                "Password must be 12-16 characters long and at least one uppercase, one lowercase, one number, and one symbol (@#$%).""")
        elif not all([old_pwd, new_pwd1, new_pwd2]) or new_pwd1 != new_pwd2:
            messages.error(request, "Invalid input or password do not match")
        elif not check_password(old_pwd, user.password):
            messages.error(request, "Incorrect current password.")
        else:
            user.set_password(new_pwd1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
    
    context = {
        'headers': headers,
        'user': user,
    }

    return render(request, "change_password.html", context)