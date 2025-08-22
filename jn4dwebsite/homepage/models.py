from django.db import models


class Header(models.Model):
    logo = models.ImageField(upload_to='images/')
    menu_item = models.CharField(max_length=100)

    def __str__(self):
        return self.name
