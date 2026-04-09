from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from homepage.forms import HeaderForm
from homepage.models import Header, Carousel, Category, Product, Item, Placeholder, UserProfile, User, ProductSize, SizeTerm
from django.contrib import messages
import os
from decimal import Decimal
from django.contrib.auth.decorators import login_required



def adminBase(request):
    headers = Header.objects.all()
    context = {
        'headers': headers
    }
    return render(request, 'admin_base.html', context)


def adminHome(request):
    # template = loader.get_template('admin_home.html')
    # return HttpResponse(template.render())
    headers = Header.objects.all()
    carousels = Carousel.objects.all()
    context = {
        'carousels': carousels,
        'headers': headers,
    }
    return render(request, 'admin_home.html', context)


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
            messages.success(request, "Header's logo and menu items are added successfully!")
            return redirect('/')
        else:
            messages.success(request, f"No Image Found. Please upload!")
            
    context = {'headers': headers}
    return render(request, 'header_page.html', context)


def editHeader(request, pk):
    headers = Header.objects.all()
    header = Header.objects.get(id=pk)

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(header.logo) > 0:
                os.remove(header.logo.path)
            header.logo = request.FILES['logo']
        header.menu_item1 = request.POST.get('menu_item1')
        header.menu_item2 = request.POST.get('menu_item2')
        header.menu_item3 = request.POST.get('menu_item3')
        header.menu_item4 = request.POST.get('menu_item4')
        header.save()
        messages.success(request, "Header Updated Successfully")
    context = {'header': header, 'headers': headers}
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
    carousels = Carousel.objects.all().order_by('id')
    context = {
        'carousels': carousels,
        'headers': headers
    }
    return render(request, 'manage_carousel.html', context)


def editCarousel(request, pk):
    headers = Header.objects.all()
    carousels = Carousel.objects.get(id=pk)

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(carousels.image) > 0:
                os.remove(carousels.image.path)
            carousels.image = request.FILES['image']
        carousels.label = request.POST.get('label')
        carousels.caption = request.POST.get('caption')
        carousels.save()
        messages.success(request, "Carousel Updated Successfully")

    context = {
        'carousels': carousels,
        'headers': headers,
    }
    return render(request, 'edit_carousel.html', context)


def addCarousel(request):
    carousels = Carousel.objects.all()
    headers = Header.objects.all()

    if request.method == "POST":
        carousel = Carousel()
        carousel.label = request.POST.get('label')
        carousel.caption = request.POST.get('caption')

        if len(request.FILES) != 0:
            carousel.image = request.FILES['image']

            carousel.save()
            messages.success(request, "New Slide Photo Saved Successfully")
            return redirect('manage-carousel')
    
        else:
            messages.success(request, f"No Image Found. Please upload!")

    context = {
        'carousels': carousels,
        'headers': headers,
    }
    return render(request, 'add_carousel.html', context)


def deleteCarousel(request, pk):
    carousels = Carousel.objects.get(id=pk)
    if len(carousels.image) > 0:
        os.remove(carousels.image.path)
    carousels.delete()
    messages.success(request, "Slide Photo deleted successfully.")
    return redirect('manage-carousel')


def manageCategories(request):
    categories = Category.objects.all().order_by('id')
    headers = Header.objects.all()
    placeholders = Placeholder.objects.all()
    context = {
        'categories': categories,
        'headers': headers,
        'placeholders': placeholders,
    }
    return render(request, 'manage_categories.html', context)


def editCategories(request, pk):
    headers = Header.objects.all()
    categories = Category.objects.get(id=pk)

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(categories.image) > 0:
                os.remove(categories.image.path)
            categories.image = request.FILES['image']
        categories.name = request.POST.get('name')
        categories.description = request.POST.get('description')
        categories.save()
        messages.success(request, "Product Category updated successfully!")
        return redirect('manage-categories')

    context = {
        'categories': categories,
        'headers': headers,
    }
    return render(request, 'edit_categories.html', context)


def addCategories(request):
    categories = Category.objects.all()
    headers = Header.objects.all()

    if request.method == "POST":
        category = Category()
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')

        if len(request.FILES) != 0:
            category.image = request.FILES['image']

            category.save()
            messages.success(request, "Product Category added successfully!")
            return redirect('manage-categories')
    
        else:
            messages.success(request, f"No Image Found. Please upload!")

    context = {
        'categories': categories,
        'headers': headers,
    }
    return render(request, 'add_categories.html', context)


def deleteCategories(request, pk):
    categories = Category.objects.get(id=pk)
    if len(categories.image) > 0:
        os.remove(categories.image.path)
    categories.delete()
    messages.success(request, "Product Category deleted successfully!")
    return redirect('manage-categories')


def addProducts(request, pk):
    headers = Header.objects.all()
    category = Category.objects.get(id=pk)
    products = Product.objects.all()

    yes_no_choices = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    if request.method == 'POST':
        product = Product()
        product.category = category
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        # product.original_price = request.POST.get('original_price')
        # product.selling_price = request.POST.get('selling_price')
        # product.quantity = request.POST.get('quantity')
        # product.sold = request.POST.get('sold')
        product.one_size = request.POST.get('yes_no_dropdown')

        if len(request.FILES) != 0:
            product.image = request.FILES['image']

            product.save()
            messages.success(request, f"{product.name} successfully added to {category.name} category {product.category_id}")
            return redirect('manage-products', product.category_id)
    
        else:
            messages.success(request, f"No Image Found. Please upload!")

    context = {
        'headers': headers,
        'category': category,
        'products': products,
        'yes_no_choices': yes_no_choices,
    }

    return render(request, 'add_products.html', context)


def manageProducts(request, pk):
    if (Category.objects.filter(id=pk)):
        headers = Header.objects.all()
        products = Product.objects.filter(category__id=pk).order_by('id')
        category = Category.objects.get(id=pk)
        context = {
            'headers': headers,
            'products': products,
            'category': category,
        }
        return render(request, 'manage_products.html', context)
    else:
        messages.warning(request, "No products found.")
        return redirect('manage-categories')

    


def editProducts(request, pk):
    headers = Header.objects.all()
    #category = Category.objects.all()
    product = Product.objects.get(id=pk)

    # yes_no_choices = [
    #     ('yes', 'Yes'),
    #     ('no', 'No'),
    # ]

    if request.method == 'POST':
        if len(request.FILES) != 0:
            if len(product.image) > 0:
                os.remove(product.image.path)
            product.image = request.FILES['image']
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        # product.quantity = request.POST.get('quantity')
        # product.sold = request.POST.get('sold')
        # product.original_price = request.POST.get('original_price')
        # product.selling_price = request.POST.get('selling_price')
        # product.one_size = request.POST.get('yes_no_dropdown')
        product.save()
        messages.success(request, f"{product.name} successfully updated {product.category_id}")
        return redirect('manage-products', product.category_id)
    context = {
        'headers': headers,
        #'category': category,
        'product': product,
        # 'yes_no_choices': yes_no_choices,
    }

    return render(request, "edit_products.html", context)


def deleteProducts(request, pk):
    product = Product.objects.get(id=pk)
    if len(product.image) > 0:
        os.remove(product.image.path)
    product.delete()
    messages.success(request, f"{product.name} successfully deleted.")    
    return redirect('manage-categories')



def manageItem(request, pk):
    if (Product.objects.filter(id=pk)):
        headers = Header.objects.all()
        items = Item.objects.filter(product__id=pk).order_by('id')
        product = Product.objects.get(id=pk)

        context = {
            'headers': headers,
            'items': items,
            'product': product,
        }

        return render(request, "manage_item.html", context)
    else:
        messages.warning(request, "No Color Product Found")
        return render(request, "manage_item.html")
    

def addItem(request, pk):
    headers = Header.objects.all()
    product = Product.objects.get(id=pk)
    category = Category.objects.get(id=product.category.id)
    item = Item.objects.all()

    if request.method == 'POST':
        item = Item()
        item.product = product
        item.category = category
        item.itemName = request.POST.get("itemName")
        item.description = request.POST.get("description")
        item.original_price = Decimal(request.POST.get("original_price").replace(',', ''))
        item.selling_price = Decimal(request.POST.get("selling_price").replace(',', ''))
        

        if (item.original_price <= item.selling_price and item.original_price > 0):
            messages.warning(request, f"Original Price must be greater than Selling Price!")
            return redirect('add-item', pk)
        else:
            # if len(request.FILES) != 0:
            if 'image' and 'image1' and 'image2' and 'image3' and 'image4' in request.FILES:
                item.image = request.FILES['image']
                item.image1 = request.FILES['image1']
                item.image2 = request.FILES['image2']
                item.image3 = request.FILES['image3']
                item.image4 = request.FILES['image4']
            
                item.save()
                messages.success(request, f"{item.itemName} successfully added to {product.name}")
                return redirect('manage-item', pk)
            else:
                messages.warning(request, f"Image is not uploaded! Please select a file.")
                # return redirect('add-item', pk)
    
    context = {
        'headers': headers,
        'product': product,
        'item': item,
    }

    return render(request, "add_item.html", context)


def editItem(request, pk):
    headers = Header.objects.all()
    item = Item.objects.get(id=pk)

    yes_no_choices = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    size_choices = [
        ('one size', 'One Size'),
        ('customize', 'Customize'),
        ('standard', 'Standard'),
    ]

    if request.method == 'POST':
        # if len(request.FILES) != 0:
        #     if len(colorProduct.image) > 0:
        #         os.remove(colorProduct.image.path)
        #     colorProduct.image = request.FILES['image']
        #     if len(colorProduct.image1) > 0:
        #         os.remove(colorProduct.image1.path)
        #     colorProduct.image1 = request.FILES['image1']
        #     if len(colorProduct.image2) > 0:
        #         os.remove(colorProduct.image2.path)
        #     colorProduct.image2 = request.FILES['image2']
        #     if len(colorProduct.image3) > 0:
        #         os.remove(colorProduct.image3.path)
        #     colorProduct.image3 = request.FILES['image3']
        #     if len(colorProduct.image4) > 0:
        #         os.remove(colorProduct.image4.path)
        #     colorProduct.image4 = request.FILES['image4'] 

        # list all image fields in your model
        image_fields = ['image', 'image1', 'image2', 'image3', 'image4']

        for field in image_fields:
            new_image = request.FILES.get(field)

            if new_image:
                # delete old file if exist
                old_image = getattr(item, field)
                if old_image and old_image.name:
                    if os.path.exists(old_image.path):
                        os.remove(old_image.path)

                #assign new image
                setattr(item, field, new_image)

        item.itemName = request.POST.get('itemName')
        item.description = request.POST.get('description')
        item.original_price = Decimal(request.POST.get('original_price').replace(',', ''))
        item.selling_price = Decimal(request.POST.get('selling_price').replace(',', ''))
        item.size = request.POST.get("size_dropdown")

        item.save()
        messages.success(request, f"{item} is edited successfully!")
        return redirect('manage-item', item.product_id)
    
    context = {
        'headers': headers,
        'item': item,
        'yes_no_choices': yes_no_choices,
        'size_choices': size_choices,
    }
    return render(request, 'edit_item.html', context)

def changeProductSize(request, pk):

    return redirect("change-product-size")

def deleteItem(request, pk):
    item = Item.objects.get(id=pk)
    if len(item.image) > 0:
        os.remove(item.image.path)
    if len(item.image1) > 0:
        os.remove(item.image1.path)
    if len(item.image2) > 0:
        os.remove(item.image2.path)
    if len(item.image3) > 0:
        os.remove(item.image3.path)
    if len(item.image4) > 0:
        os.remove(item.image4.path)
    item.delete()
    messages.warning(request, f"{item.itemName} has been deleted!")
    return redirect('manage-item', item.product_id)


def manageItemImages(request, pk):
    
    if (Item.objects.filter(id=pk)):
        headers = Header.objects.all()
        items = Item.objects.filter(id=pk)
        item = Item.objects.get(id=pk)
        product = Product.objects.get(id=item.product.id)
        placeholders = Placeholder.objects.all()
        
        context = {
            'headers': headers,
            'items': items,
            'product': product,
            'placeholders': placeholders,
        }
        return render(request, 'manage_item_images.html', context)
    else:
        messages.warning(request, "No Image Found")
        return render(request, 'manage_item_images.html')
    

def editPlaceholder(request, pk):
    headers = Header.objects.all()
    placeholders = Placeholder.objects.all()
    placeholder = Placeholder.objects.get(id=pk)

    if request.method == 'POST':
        if len(request.FILES) != 0:
            if len(placeholder.image) > 0:
                os.remove(placeholder.image.path)   
            placeholder.image = request.FILES['image']
        placeholder.label = request.POST.get('label')
        placeholder.save()
        messages.success(request, "Placeholder updated successfully!")

    context = {
        'headers': headers,
        'placeholders': placeholders,
        'placeholder': placeholder,
    }

    return render(request, 'edit_placeholder.html', context)


def addPlaceholder(request):
    # categories = Category.objects.all()
    headers = Header.objects.all()
    # placeholders = Placeholder.objects.all()

    if request.method == "POST":
        placeholder = Placeholder()
        placeholder.label = request.POST.get("label")

        if len(request.FILES) != 0:
            placeholder.image = request.FILES['image']

            placeholder.save()
            messages.success(request, "Placeholder added succesfully!")
            # return redirect('manage-categories')
        
        else:
            messages.success(request, "No image Found. Please upload!")

    context = {
        # 'categories': categories,
        'headers': headers,
        # 'placeholders': placeholders,
    }
    return render(request, 'add_placeholder.html', context)


def deletePlaceholder(request, pk):
    placeholder = Placeholder.objects.get(id=pk)
    if len(placeholder.image) > 0:
        os.remove(placeholder.image.path)
    placeholder.delete()
    messages.success(request, "Placeholder is deleted successfully!")
    return redirect('manage-categories')

@login_required
def manageUsers(request):
    headers = Header.objects.all()
    userprofile = UserProfile.objects.all().order_by('user_id')
    # user = User.objects.all()

    status_choices = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    role_choices = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('customer', 'Customer')
    ]

    context = {
        'headers': headers,
        'userprofile': userprofile,
        'status_choices': status_choices,
        'role_choices': role_choices,
        # 'user': user,
    }

    return render(request, 'manage_users.html', context)



@login_required
def changeUserStatus(request, pk):
    if request.method == "POST":
        status = request.POST.get("status_dropdown")
        userprofile = UserProfile.objects.get(user_id=pk)
        userprofile.status = status
        userprofile.save()

        messages.success(request, "Status updated successfully!")
        return redirect("manage-users")
    

@login_required
def changeUserRole(request, pk):
    if request.method == "POST":
        role = request.POST.get("role_dropdown")
        userprofile = UserProfile.objects.get(user_id=pk)
        user = User.objects.get(id=pk)
        userprofile.role = role
        if role == "admin":
            user.is_staff = "t"
            user.is_superuser = "t"
            user.save()
        elif role == "employee":
            user.is_staff = "t"
            user.is_superuser = "f"
            user.save()
        else:
            user.is_staff = "f"
            user.save()
        userprofile.save()

        messages.success(request, "Role updated successfully!")
        return redirect("manage-users")

def manageProductSize(request):
    headers = Header.objects.all()
    productSize = ProductSize.objects.all().order_by('id')

    context = {
        'headers': headers,
        'productSize': productSize,
    }

    return render(request, 'manage_product_size.html', context)

def editProductSize(request, pk):
    headers = Header.objects.all()
    productSize = ProductSize.objects.get(id=pk)

    if request.method == "POST":
        productSize.name = request.POST.get('name')
        productSize.description = request.POST.get('description')
        productSize.save()
        messages.success(request, f"{productSize.name} updated successfully!")
        return redirect('manage-product-size')

    context = {
        'headers': headers,
        'productSize': productSize,
    }

    return render(request, 'edit_product_size.html', context)

def addProductSize(request):
    headers = Header.objects.all()
    productSize = ProductSize.objects.all()

    if request.method == "POST":
        prodSize = ProductSize()
        prodSize.name = request.POST.get("name")
        prodSize.description = request.POST.get("description")
        prodSize.save()
        messages.success(request, f"{prodSize.name} successfully added!")
        return redirect('manage-product-size')

    context = {
        'headers': headers,
        'productSize': productSize,
    }

    return render(request, "add_product_size.html", context)

def deleteProductSize(request, pk):
    productSize = ProductSize.objects.get(id=pk)
    productSize.delete()
    messages.success(request, f"{productSize.name} has been deleted.")
    return redirect('manage-product-size')


def manageSizeTerm(request, pk):
    if(ProductSize.objects.filter(id=pk)):
        headers = Header.objects.all()
        sizeTerm = SizeTerm.objects.filter(productSize__id=pk).order_by('id')
        productSize = ProductSize.objects.get(id=pk)

        context = {
            'headers': headers,
            'sizeTerm': sizeTerm,
            'productSize': productSize
        }

        return render(request, 'manage_size_term.html', context)
    else:
        messages.warning(request, "No Size Term found")
        return render(request, "manage_size_term.html")
    
def addSizeTerm(request, pk):
    headers = Header.objects.all()
    productSize = ProductSize.objects.get(id=pk)
    sizeTerm = SizeTerm.objects.all()

    if request.method == 'POST':
        sizeTerm = SizeTerm()
        sizeTerm.productSize = productSize
        sizeTerm.name = request.POST.get("name")
        sizeTerm.description = request.POST.get("description")
        sizeTerm.acronym = request.POST.get("acronym")
        sizeTerm.save()
        messages.success(request, f"{sizeTerm.name} has been added.")
        return redirect('manage-size-term', productSize.id)

    context = {
        'headers': headers,
        'productSize': productSize,
        'sizeTerm': sizeTerm,
    }

    return render(request, 'add_size_term.html', context)

def editSizeTerm(request, pk):
    headers = Header.objects.all()
    sizeTerm = SizeTerm.objects.get(id=pk)
    productSize = ProductSize.objects.get(id=sizeTerm.productSize_id)

    if request.method == "POST":
        sizeTerm.acronym = request.POST.get('acronym')
        sizeTerm.name = request.POST.get('name')
        sizeTerm.description = request.POST.get('description')
        sizeTerm.save()
        messages.success(request, f"{sizeTerm.name} has been updated.")
        return redirect('manage-size-term', productSize.id)

    context = {
        'headers': headers,
        'sizeTerm': sizeTerm,
        'productSize': productSize,
    }
    return render(request, 'edit_size_term.html', context)

def deleteSizeTerm(request, pk):
    sizeTerm = SizeTerm.objects.get(id=pk)
    productSize = ProductSize.objects.get(id=sizeTerm.productSize_id)
    sizeTerm.delete()
    messages.success(request, f"{sizeTerm.name} has been deleted.")
    return redirect('manage-size-term', productSize.id)
    
    