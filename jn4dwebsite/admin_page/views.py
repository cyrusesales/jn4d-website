from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from homepage.forms import HeaderForm
from homepage.models import Header, Carousel, Category, Product, ColorProduct, Placeholder
from django.contrib import messages
import os
from decimal import Decimal


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

    yes_no_choices = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    if request.method == 'POST':
        if len(request.FILES) != 0:
            if len(product.image) > 0:
                os.remove(product.image.path)
            product.image = request.FILES['image']
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.quantity = request.POST.get('quantity')
        product.sold = request.POST.get('sold')
        product.original_price = request.POST.get('original_price')
        product.selling_price = request.POST.get('selling_price')
        product.one_size = request.POST.get('yes_no_dropdown')
        product.save()
        messages.success(request, f"{product.name} successfully updated {product.category_id}")
        return redirect('manage-products', product.category_id)
    context = {
        'headers': headers,
        #'category': category,
        'product': product,
        'yes_no_choices': yes_no_choices,
    }

    return render(request, "edit_products.html", context)


def deleteProducts(request, pk):
    product = Product.objects.get(id=pk)
    if len(product.image) > 0:
        os.remove(product.image.path)
    product.delete()
    messages.success(request, f"{product.name} successfully deleted.")    
    return redirect('manage-categories')



def manageColorProduct(request, pk):
    if (Product.objects.filter(id=pk)):
        headers = Header.objects.all()
        colorProducts = ColorProduct.objects.filter(product__id=pk).order_by('id')
        product = Product.objects.get(id=pk)

        context = {
            'headers': headers,
            'colorProducts': colorProducts,
            'product': product,
        }

        return render(request, "manage_color_product.html", context)
    else:
        messages.warning(request, "No Color Product Found")
        return render(request, "manage_color_product.html")
    

def addColorProduct(request, pk):
    headers = Header.objects.all()
    product = Product.objects.get(id=pk)
    category = Category.objects.get(id=product.category.id)
    colorProduct = ColorProduct.objects.all()

    if request.method == 'POST':
        colorProduct = ColorProduct()
        colorProduct.product = product
        colorProduct.category = category
        colorProduct.colorName = request.POST.get("colorName")
        colorProduct.description = request.POST.get("description")
        colorProduct.original_price = Decimal(request.POST.get("original_price").replace(',', ''))
        colorProduct.selling_price = Decimal(request.POST.get("selling_price").replace(',', ''))

        if (colorProduct.original_price <= colorProduct.selling_price):
            messages.warning(request, f"Original Price must be greater than Selling Price!")
            return redirect('add-color-product', pk)
        else:
            # if len(request.FILES) != 0:
            if 'image' and 'image1' and 'image2' and 'image3' and 'image4' in request.FILES:
                colorProduct.image = request.FILES['image']
                colorProduct.image1 = request.FILES['image1']
                colorProduct.image2 = request.FILES['image2']
                colorProduct.image3 = request.FILES['image3']
                colorProduct.image4 = request.FILES['image4']
            
                colorProduct.save()
                messages.success(request, f"{colorProduct.colorName} successfully added to {product.name}")
                # return redirect('manage-color-product', pk)
            else:
                messages.warning(request, f"Image is not uploaded! Please select a file.")
                # return redirect('add-color-product', pk)
    
    context = {
        'headers': headers,
        'product': product,
        'colorProduct': colorProduct,
    }

    return render(request, "add_color_product.html", context)


def editColorProduct(request, pk):
    headers = Header.objects.all()
    colorProduct = ColorProduct.objects.get(id=pk)

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
                old_image = getattr(colorProduct, field)
                if old_image and old_image.name:
                    if os.path.exists(old_image.path):
                        os.remove(old_image.path)

                #assign new image
                setattr(colorProduct, field, new_image)

        colorProduct.colorName = request.POST.get('colorName')
        colorProduct.description = request.POST.get('description')
        colorProduct.original_price = Decimal(request.POST.get('original_price').replace(',', ''))
        colorProduct.selling_price = Decimal(request.POST.get('selling_price').replace(',', ''))

        colorProduct.save()
        messages.success(request, f"{colorProduct} is edited successfully!")
        return redirect('manage-color-product', colorProduct.product_id)
    
    context = {
        'headers': headers,
        'colorProduct': colorProduct,
    }

    return render(request, 'edit_color_product.html', context)

def deleteColorProduct(request, pk):
    colorProduct = ColorProduct.objects.get(id=pk)
    if len(colorProduct.image) > 0:
        os.remove(colorProduct.image.path)
    if len(colorProduct.image1) > 0:
        os.remove(colorProduct.image1.path)
    if len(colorProduct.image2) > 0:
        os.remove(colorProduct.image2.path)
    if len(colorProduct.image3) > 0:
        os.remove(colorProduct.image3.path)
    if len(colorProduct.image4) > 0:
        os.remove(colorProduct.image4.path)
    colorProduct.delete()
    messages.warning(request, f"{colorProduct.colorName} has been deleted!")
    return redirect('manage-color-product', colorProduct.product_id)


def manageColorProductImages(request, pk):
    
    if (ColorProduct.objects.filter(id=pk)):
        headers = Header.objects.all()
        colorProducts = ColorProduct.objects.filter(id=pk)
        colorProduct = ColorProduct.objects.get(id=pk)
        product = Product.objects.get(id=colorProduct.product.id)
        placeholders = Placeholder.objects.all()
        
        context = {
            'headers': headers,
            'colorProducts': colorProducts,
            'product': product,
            'placeholders': placeholders,
        }
        return render(request, 'manage_color_product_images.html', context)
    else:
        messages.warning(request, "No Image Found")
        return render(request, 'manage_color_product_images.html')
    

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
