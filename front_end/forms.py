from django import forms
from .models import Ship, Area


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Ship
        fields = '__all__'
