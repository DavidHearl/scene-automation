from django import forms
from .models import Ship, Area

class ShipForm(forms.ModelForm):
    class Meta:
        model = Ship
        fields = ['name', 'contract_number', 'company']


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'