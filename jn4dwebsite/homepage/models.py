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
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.id
