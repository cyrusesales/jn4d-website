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
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.id


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    description = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(null=True, blank=True)
    original_price = models.FloatField(null=True, blank=True)
    selling_price = models.FloatField(null=True, blank=True)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    tag = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id