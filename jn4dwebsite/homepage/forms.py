from django import forms
from .models import Header


class HeaderForm(forms.ModelForm):
    class Meta:
        model = Header
        fields = ['logo', 'menu_item1',
                  'menu_item2', 'menu_item3', 'menu_item4']
