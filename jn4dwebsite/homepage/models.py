from django.db import models


class Header(models.Model):
    logo = models.ImageField(upload_to='images/')
    menu_item1 = models.CharField(max_length=100, blank=True, null=True)
    menu_item2 = models.CharField(max_length=100, blank=True, null=True)
    menu_item3 = models.CharField(max_length=100, blank=True, null=True)
    menu_item4 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.id


class Carousel(models.Model):
    image = models.ImageField(upload_to='images/')
    label = models.CharField(max_length=100, blank=True, null=True)
    caption = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.id


class Category(models.Model):
    image = models.ImageField(upload_to='categories/')
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return str(self.name or self.id)

class Placeholder(models.Model):
    image = models.ImageField(upload_to='placeholder/')
    label = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.label or self.id)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #slug = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    description = models.CharField(max_length=300, blank=True, null=True)
    # quantity = models.IntegerField(null=True, blank=True)
    # sold = models.IntegerField(null=True, blank=True)
    # original_price = models.FloatField(null=True, blank=True)
    # selling_price = models.FloatField(null=True, blank=True)
    one_size = models.CharField(max_length=100, blank=True, null=True)
    #one_size = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    #trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    #tag = models.CharField(max_length=100, null=True, blank=True)
    #created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name or self.id)
    
class ColorProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    colorName = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='colorproducts/',blank=True, null=True)
    image1 = models.ImageField(upload_to='colorproducts/',blank=True, null=True)
    image2 = models.ImageField(upload_to='colorproducts/',blank=True, null=True)
    image3 = models.ImageField(upload_to='colorproducts/',blank=True, null=True)
    image4 = models.ImageField(upload_to='colorproducts/',blank=True, null=True)
    original_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.colorName or self.id)